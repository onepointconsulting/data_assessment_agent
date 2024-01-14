from typing import Union, Any, List

import asyncio

import sys
from typing import Callable

from psycopg import AsyncCursor, AsyncConnection
from psycopg_pool import AsyncConnectionPool
from data_assessment_agent.config.config import db_cfg
from data_assessment_agent.model.db_model import (
    QuestionnaireStatus,
    TopicScore,
    QuestionScore,
    Question,
    Topic,
    TotalScore,
    SessionReport,
    QuizzMode,
    SelectedConfiguration
)
from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.model.assessment_framework import SuggestedResponse


def create_pool():
    async_pool = AsyncConnectionPool(conninfo=db_cfg.db_conn_str, open=False)
    logger.info("Using %s", db_cfg.db_conn_str)
    return async_pool


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asynch_pool = create_pool()


async def open_pool():
    try:
        await asynch_pool.open()
        await asynch_pool.wait()
        logger.info("Asynch connection pool Opened")
    except:
        logger.error("Could not open pool")


asyncio.run(open_pool())


async def close_pool():
    logger.info("Trying to close asynch pool")
    try:
        await asynch_pool.close()
        logger.info("Closed asynch pool")
    except:
        logger.exception("Could not close pool")


async def create_cursor(func: Callable) -> Any:
    # await asynch_pool.check()
    try:
        conn = await AsyncConnection.connect(conninfo=db_cfg.db_conn_str)
        # async with asynch_pool.connection() as conn:
        async with conn.cursor() as cur:
            return await func(cur)
    except:
        logger.exception("Could not create cursor.")
    finally:
        if conn is not None:
            await conn.close()


async def execute_on_connection(func: Callable) -> Any:
    # await asynch_pool.check()
    try:
        conn = await AsyncConnection.connect(conninfo=db_cfg.db_conn_str)
        await func(conn)
    except:
        logger.exception("Could not open connection.")
    finally:
        if conn is not None:
            await conn.close()


async def handle_select_func(query: str, query_params: dict):
    async def func(cur: AsyncCursor):
        await cur.execute(
            query,
            query_params,
        )
        return list(await cur.fetchall())

    return func


async def select_from(query: str, parameter_map: dict) -> list:
    handle_select = await handle_select_func(query, parameter_map)
    return await create_cursor(handle_select)


async def select_last_question(session_id: str) -> Union[QuestionnaireStatus, None]:
    async def handle_select(cur: AsyncCursor):
        await cur.execute(
            """
SELECT S.ID,
	S.SESSION_ID,
	S.TOPIC,
	S.QUESTION,
	S.ANSWER,
	S.SCORE,
	S.CREATED_AT,

	(SELECT COUNT(DISTINCT(QS1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS1
		WHERE QS1.SESSION_ID = %(session_id)s
			AND QS1.TOPIC = S.TOPIC
			AND ANSWER IS NOT NULL) TOPIC_COUNT,

	(SELECT T.QUESTION_AMOUNT - COUNT(DISTINCT(QS1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS1
		WHERE QS1.SESSION_ID = %(session_id)s
			AND QS1.TOPIC = S.TOPIC
			AND QS1.ANSWER IS NOT NULL) TOPIC_MISSING,

    (SELECT COUNT(*) FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS2
		WHERE QS2.QUESTION = S.QUESTION AND QS2.SESSION_ID = S.SESSION_ID 
	 		AND QS2.ANSWER IS NOT NULL) PREVIOUS_ANSWER_COUNT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S
INNER JOIN TB_TOPIC T ON T.NAME = S.TOPIC
WHERE SESSION_ID = %(session_id)s
ORDER BY ID DESC
LIMIT 1""",
            {"session_id": session_id},
        )
        return list(await cur.fetchall())

    statuses: list = await create_cursor(handle_select)
    if len(statuses) == 0:
        return None
    (
        id,
        db_session_id,
        topic,
        question,
        answer,
        score,
        created_at,
        topic_count,
        topic_missing,
        previous_answer_count,
    ) = statuses[0]
    return QuestionnaireStatus(
        id=id,
        session_id=db_session_id,
        topic=topic,
        question=question,
        answer=answer,
        score=score,
        created_at=created_at,
        topic_count=topic_count,
        topic_missing=topic_missing,
        previous_answer_count=previous_answer_count,
    )


async def select_random_session() -> Union[str, None]:
    async def handle_select(cur: AsyncCursor):
        await cur.execute(
            """
select session_id from public.tb_questionnaire_status order by random() limit 1
"""
        )
        return list(await cur.fetchall())

    session_ids: list = await create_cursor(handle_select)
    if len(session_ids) > 0:
        return session_ids[0][0]
    return None


async def select_last_empty_question(
    session_id: str,
) -> Union[QuestionnaireStatus, None]:
    query = """
SELECT ID,
	SESSION_ID,
	TOPIC,
	QUESTION,
	CREATED_AT
FROM TB_QUESTIONNAIRE_STATUS
WHERE SESSION_ID = %(session_id)s
	AND ANSWER IS NULL
ORDER BY ID DESC
LIMIT 1
"""
    parameter_map = {"session_id": session_id}
    unanswered_questions: list = await select_from(query, parameter_map)
    if len(unanswered_questions) > 0:
        (id, session_id, topic, question, _) = unanswered_questions[0]
        return QuestionnaireStatus(
            id=id, session_id=session_id, topic=topic, question=question
        )
    return None


async def select_topic_scores(session_id: str) -> List[TopicScore]:
    query = """
SELECT T.NAME AS TOPIC_NAME,
	COALESCE(MAX_SCORE, 0),
	COALESCE(SCORE,0) SCORE
FROM TB_TOPIC T
LEFT JOIN
	(SELECT TOPIC_NAME,
			SUM(MAX_SCORE) AS MAX_SCORE,
			SUM(SCORE) AS SCORE
		FROM VW_QUESTION_SCORES
		WHERE SESSION_ID = %(session_id)s
		GROUP BY TOPIC_NAME) TOPIC_COUNTS ON TOPIC_COUNTS.TOPIC_NAME = T.NAME;
"""
    parameter_map = {"session_id": session_id}
    topic_scores_raw: list = await select_from(query, parameter_map)
    if topic_scores_raw is None:
        return []
    return [
        TopicScore(topic_name=topic_name, max_score=max_score, score=score)
        for (topic_name, max_score, score) in topic_scores_raw
    ]


async def select_question_scores(session_id: str) -> Union[List[QuestionScore], None]:
    query = """
select score, max_score, sentiment_name, topic_name, session_id from vw_question_scores where session_id = %(session_id)s
"""
    parameter_map = {"session_id": session_id}
    scores_raw: list = await select_from(query, parameter_map)
    return [
        QuestionScore(
            score=score,
            max_score=max_score,
            sentiment_name=sentiment_name,
            topic_name=topic_name,
            session_id=session_id,
        )
        for (score, max_score, sentiment_name, topic_name, session_id) in scores_raw
    ]


async def select_initial_question_from_topic(
    topic: str, session_id
) -> Union[Question, None]:
    # This query makes sure the an hallucinated topic is replaced by a random topic.
    query = """
SELECT Q.ID,
	Q.QUESTION,
	Q.SCORE,
	Q.TOPIC_ID,
	T.NAME TOPIC_NAME,
	T.DESCRIPTION TOPIC_DESCRIPTION,

	(SELECT COUNT(*)
		FROM TB_QUESTION
		WHERE TOPIC_ID = T.ID) TOPIC_COUNT
FROM TB_QUESTION Q
INNER JOIN TB_TOPIC T ON Q.TOPIC_ID = T.ID
WHERE T.NAME = (
    SELECT COALESCE(
        (SELECT NAME
            FROM TB_TOPIC
            WHERE NAME = %(topic)s AND NAME NOT IN
                    (SELECT TOPIC
                        FROM TB_QUESTIONNAIRE_STATUS
                        WHERE SESSION_ID = %(session_id)s)),
        (SELECT NAME -- Go for the random topic, if the topic here does not exist in the database
            FROM TB_TOPIC
            WHERE NAME NOT IN
                    (SELECT TOPIC
                        FROM TB_QUESTIONNAIRE_STATUS
                        WHERE SESSION_ID = %(session_id)s)
            ORDER BY RANDOM() LIMIT 1))
)
ORDER BY preferred_question_order
LIMIT 1
"""
    parameter_map = {"topic": topic, "session_id": session_id}
    questions: list = await select_from(query, parameter_map)
    if len(questions) > 0:
        (id, question, score, topic_id, topic_name, topic_description, _) = questions[0]
        topic = Topic(id=topic_id, name=topic_name, description=topic_description)
        question = Question(id=id, question=question, score=score, topic=topic)
        return question
    else:
        return None


async def calculate_simple_total_score(session_id: str) -> TotalScore:
    query = """
SELECT SUM(SCORE) TOTAL_SCORE,
	SUM(MAX_SCORE) MAX_SCORE,
	(SUM(SCORE * 1.0) / SUM(MAX_SCORE)) * 100 PCT_SCORE
FROM VW_QUESTION_SCORES
WHERE SESSION_ID = %(session_id)s
"""
    parameter_map = {"session_id": session_id}
    scoring: list = await select_from(query, parameter_map)
    if len(scoring) > 0:
        (total_score, max_score, pct_score) = scoring[0]
        return TotalScore(
            total_score=total_score, max_score=max_score, pct_score=pct_score
        )
    return TotalScore(total_score=0, max_score=0, pct_score=0.0)


async def select_session_report(session_id: str) -> List[SessionReport]:
    query = """
SELECT TOPIC_NAME,
	QUESTION,
	ANSWER,
	SCORE,
	SENTIMENT_NAME,
	CREATED_AT,
	UPDATED_AT
FROM VW_QUESTION_SCORES
WHERE SESSION_ID = %(session_id)s AND ANSWER IS NOT NULL and TOPIC_NAME IS NOT NULL
"""
    parameter_map = {"session_id": session_id}
    report_list: list = await select_from(query, parameter_map)
    return [
        SessionReport(
            topic=topic,
            question=question,
            answer=answer,
            score=score,
            sentiment=sentiment,
            created_at=created_at,
            updated_at=updated_at,
        )
        for (
            topic,
            question,
            answer,
            score,
            sentiment,
            created_at,
            updated_at,
        ) in report_list
    ]


async def select_topics() -> List[str]:
    query = """SELECT NAME FROM TB_TOPIC ORDER BY NAME"""
    topics: list = await select_from(query, {})
    return [t[0] for t in topics]


async def select_suggestions(question: str, topic: str) -> List[SuggestedResponse]:
    query = """
SELECT Q.ID, Q.QUESTION, Q.SCORE, T.ID, T.NAME, T.DESCRIPTION, S.ID, S.TITLE, S.SUBTITLE, S.BODY
FROM TB_SUGGESTED_RESPONSE S
INNER JOIN TB_QUESTION Q ON Q.ID = S.QUESTION_ID
INNER JOIN TB_TOPIC T ON T.ID = Q.TOPIC_ID
WHERE Q.QUESTION = %(question)s
	AND T.NAME = %(topic)s order by S.TITLE desc
"""
    parameter_map = {"question": question, "topic": topic}
    response_list: list = await select_from(query, parameter_map)
    return [
        SuggestedResponse(
            title=suggestion_title, subtitle=suggestion_subtitle, body=suggestion_body
        )
        for (
            _,
            _,
            _,
            _,
            _,
            _,
            _,
            suggestion_title,
            suggestion_subtitle,
            suggestion_body,
        ) in response_list
    ]


async def has_selected_topics(session_id: str) -> bool:
    query = """SELECT COUNT(*) FROM PUBLIC.TB_SELECTED_TOPICS WHERE SESSION_ID = %(session_id)s"""
    parameter_map = {"session_id": session_id}
    response = await select_from(query, parameter_map)
    return response[0][0] > 0


async def insert_selected_configuration(
    configuration: SelectedConfiguration
):
    session_id = configuration.session_id
    topic_list = configuration.topic_list
    quiz_mode_name = configuration.quiz_mode_name
    logger.info("session_id: %s", session_id)
    logger.info("topic_list: %s", topic_list)
    logger.info("quiz_mode_name: %s", quiz_mode_name)
    async def process_selected_topics(conn: AsyncConnection):
        query1 = """
insert into public.tb_selected_topics(session_id, topic_id, created_at)
values(%s, (select id from public.tb_topic where name=%s), now())
"""
        query_quiz_mode = """
insert into tb_selected_quiz_mode(session_id, quiz_mode_id)
values(%(session_id)s, (select id from tb_quiz_mode where name = %(quiz_mode_name)s))
"""
        data = [(session_id, t) for t in topic_list]
        async with conn.cursor() as cur:
            await cur.executemany(query1, data)
            await cur.execute(query_quiz_mode, {"session_id": session_id, "quiz_mode_name": quiz_mode_name})
            await conn.commit()

    await execute_on_connection(process_selected_topics)


async def select_quiz_modes() -> List[QuizzMode]:
    query = """select id, name, question_count from tb_quiz_mode"""
    response = await select_from(query, {})
    return [QuizzMode(id=r[0], name=r[1], question_count=r[2]) for r in response]


if __name__ == "__main__":

    async def test_select_last_session():
        session_id = await select_random_session()
        logger.info(session_id)
        last_question = await select_last_question(session_id)
        logger.info(last_question)

    async def test_select_last_empty_question():
        session_id = await select_random_session()
        logger.info(session_id)
        last_empty = await select_last_empty_question(session_id)
        logger.info(last_empty)

    async def test_select_topic_scores():
        session_id = await select_random_session()
        logger.info(session_id)
        topic_scores = await select_topic_scores(session_id)
        for topic_score in topic_scores:
            logger.info(topic_score)

    async def test_select_question_scores():
        session_id = await select_random_session()
        logger.info(session_id)
        topic_scores = await select_question_scores(session_id)
        for topic_score in topic_scores:
            logger.info(topic_score)

    async def test_select_suggestions():
        logger.info("=== Suggestions ===")
        suggestions = await select_suggestions(
            "What are the organization's overall business goals and objectives?",
            "Business Alignment",
        )
        for s in suggestions:
            print(s)

    async def test_select_topics():
        print("=== Topics ===")
        topics = await select_topics()
        for s in topics:
            print(s)

    async def test_has_selected_topics():
        res = await has_selected_topics("dummy")
        assert res is False

    async def test_insert_into_selected_topics():
        topics = await select_topics()
        topics = topics[:2]
        dummy_session_id = "dummy"
        quiz_mode_name = "Medium"
        selected_configuration = SelectedConfiguration(session_id=dummy_session_id, quiz_mode_name=quiz_mode_name, topic_list=topics)
        await insert_selected_configuration(selected_configuration)

    async def test_quizz_modes():
        quizz_modes = await select_quiz_modes()
        assert quizz_modes is not None
        for quizz_mode in quizz_modes:
            print(quizz_mode.model_dump_json())
    
    
    # asyncio.run(test_select_topic_scores())
    # asyncio.run(test_select_question_scores())
    # asyncio.run(test_select_suggestions())
    # asyncio.run(test_select_topics())
    # asyncio.run(test_has_selected_topics())
    asyncio.run(test_insert_into_selected_topics())
    # asyncio.run(test_quizz_modes())
