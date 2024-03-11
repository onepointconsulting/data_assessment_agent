from typing import Union, Any, List, Optional

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
    SelectedConfiguration,
    QuestionnaireCounts,
    QAScored,
)
from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.model.assessment_framework import SuggestedResponse


QUESTION_FILTER = "(Q.YES_NO_QUESTION != false OR Q.SCORED != false)"


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


async def create_cursor(func: Callable, commit=False) -> Any:
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
            if commit:
                await conn.commit()
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


async def select_initial_question(session_id: str) -> Union[Question, None]:
    query = f"""
SELECT Q.ID,
	Q.QUESTION,
	Q.SCORE,
	T.ID TOPIC_ID,
	T.NAME TOPIC_NAME,
	T.DESCRIPTION TOPIC_DESCRIPTION,
	T.QUESTION_AMOUNT,
    Q.YES_NO_QUESTION
FROM TB_QUESTION Q
INNER JOIN PUBLIC.TB_TOPIC T ON T.ID = Q.TOPIC_ID
INNER JOIN PUBLIC.TB_SELECTED_TOPICS ST ON ST.TOPIC_ID = T.ID
WHERE ST.SESSION_ID = %(session_id)s AND {QUESTION_FILTER}
ORDER BY Q.ID LIMIT 1
"""
    parameter_map = {"session_id": session_id}
    questions: list = await select_from(query, parameter_map)
    if len(questions) > 0:
        (
            question_id,
            question_question,
            question_score,
            topic_id,
            topic_name,
            topic_description,
            question_amount,
            yes_no_question,
        ) = questions[0]
        topic = Topic(id=topic_id, name=topic_name, topic_description=topic_description)
        return Question(
            id=question_id,
            question=question_question,
            score=question_score,
            topic=topic,
            yes_no_question=yes_no_question,
        )
    return None


async def select_remaining_questions(
    session_id: str, topic: str
) -> Union[List[str], None]:
    query = f"""
SELECT Q.QUESTION
FROM PUBLIC.TB_QUESTION Q
INNER JOIN PUBLIC.TB_TOPIC T ON Q.TOPIC_ID = T.ID
WHERE T.NAME = %(topic)s
    AND {QUESTION_FILTER}
	AND NOT EXISTS
		(SELECT QUESTION
			FROM PUBLIC.TB_QUESTIONNAIRE_STATUS
			WHERE SESSION_ID = %(session_id)s
				AND Q.QUESTION = QUESTION
				AND TOPIC = %(topic)s
                AND ANSWER IS NOT NULL
			GROUP BY QUESTION)"""
    logger.info("select_remaining_questions: %s", query)
    parameter_map = {"session_id": session_id, "topic": topic}
    questions: list = await select_from(query, parameter_map)
    return [q[0] for q in questions]


async def handle_question_answers_select(
    query: str, parameter_map: dict
) -> Union[List[str], None]:
    answered_questions: list = await select_from(query, parameter_map)
    return [f"{t[0]}\n{t[1]}" for t in answered_questions]


async def select_answered_questions_in_topic(
    session_id: str, topic: str
) -> Union[List[str], None]:
    query = """
SELECT QUESTION,
	(SELECT ANSWER
		FROM TB_QUESTIONNAIRE_STATUS
		WHERE ID = MAX(S.ID))
FROM TB_QUESTIONNAIRE_STATUS S
WHERE SESSION_ID = %(session_id)s
	AND TOPIC = %(topic)s
	AND ANSWER IS NOT NULL
GROUP BY QUESTION"""
    parameter_map = {"session_id": session_id, "topic": topic}
    return await handle_question_answers_select(query, parameter_map)


async def select_answered_questions_in_session(
    session_id: str,
) -> Union[List[str], None]:
    query = """
SELECT S.QUESTION,
	S.ANSWER
FROM TB_QUESTIONNAIRE_STATUS S
WHERE SESSION_ID = %(session_id)s
	AND S.ANSWER IS NOT NULL
ORDER BY S.ID"""
    parameter_map = {"session_id": session_id}
    return await handle_question_answers_select(query, parameter_map)


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

	(SELECT
			(SELECT QM.QUESTION_COUNT
				FROM PUBLIC.TB_QUIZ_MODE QM
				INNER JOIN PUBLIC.TB_SELECTED_QUIZ_MODE SQM ON QM.ID = SQM.quiz_mode_id
				WHERE SQM.SESSION_ID = %(session_id)s) - COUNT(DISTINCT(QS1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS1
		WHERE QS1.SESSION_ID = %(session_id)s
			AND QS1.TOPIC = S.TOPIC
			AND QS1.ANSWER IS NOT NULL) TOPIC_MISSING,

	(SELECT COUNT(*)
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS2
		WHERE QS2.QUESTION = S.QUESTION
			AND QS2.SESSION_ID = S.SESSION_ID
			AND QS2.ANSWER IS NOT NULL) PREVIOUS_ANSWER_COUNT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S
INNER JOIN TB_TOPIC T ON T.NAME = S.TOPIC
WHERE SESSION_ID = %(session_id)s
ORDER BY ID DESC
LIMIT 1
""",
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
SELECT ST.SESSION_ID
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS
INNER JOIN PUBLIC.TB_TOPIC T ON QS.TOPIC = T.NAME
INNER JOIN PUBLIC.TB_SELECTED_TOPICS ST ON ST.TOPIC_ID = T.ID
WHERE ANSWER IS NOT NULL
ORDER BY RANDOM()
LIMIT 1
"""
        )
        return list(await cur.fetchall())

    session_ids: list = await create_cursor(handle_select)
    if len(session_ids) > 0:
        return session_ids[0][0]
    return None


async def select_random_question() -> Union[Question, None]:
    query = f"""
SELECT Q.ID,
	QUESTION,
	SCORE,
	TOPIC_ID,
	PREFERRED_QUESTION_ORDER,
	YES_NO_QUESTION,
	SCORED,
	T.NAME
FROM TB_QUESTION Q
INNER JOIN TB_TOPIC T ON Q.TOPIC_ID = T.ID
WHERE {QUESTION_FILTER}
ORDER BY RANDOM()
LIMIT 1
"""
    parameter_map = {}
    questions = await select_from(query, parameter_map)
    if len(questions) > 0:
        (
            id,
            question,
            score,
            topic_id,
            preferred_question_order,
            yes_no_question,
            scored,
            topic_name,
        ) = questions[0]
        topic = Topic(id=topic_id, name=topic_name)
        question = Question(
            id=id,
            question=question,
            score=score,
            topic=topic,
            preferred_order=preferred_question_order,
            yes_no_question=yes_no_question,
            scored=scored,
        )
        return question
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
	COALESCE(MAX_SCORE, 0) MAX_SCORE,
	COALESCE(SCORE, 0) SCORE
FROM TB_TOPIC T
INNER JOIN PUBLIC.TB_SELECTED_TOPICS ST ON ST.TOPIC_ID = T.ID
LEFT JOIN
(SELECT TOPIC TOPIC_NAME,
	SUM(QS.SCORE) SCORE,
	SUM(CASE WHEN Q.SCORED = TRUE and QS.ANSWER IS NOT NULL THEN 1 ELSE 0 END) * 10 MAX_SCORE
FROM TB_QUESTIONNAIRE_STATUS QS
INNER JOIN PUBLIC.TB_TOPIC T ON T.NAME = QS.TOPIC
INNER JOIN PUBLIC.TB_QUESTION Q ON Q.QUESTION = QS.QUESTION AND Q.SCORED = true
AND Q.TOPIC_ID = T.ID
WHERE SESSION_ID = %(session_id)s
GROUP BY QS.TOPIC) TOPIC_COUNTS ON TOPIC_COUNTS.TOPIC_NAME = T.NAME
WHERE ST.SESSION_ID = %(session_id)s
"""
    parameter_map = {"session_id": session_id}
    topic_scores_raw: list = await select_from(query, parameter_map)
    if topic_scores_raw is None:
        return []
    return [
        TopicScore(topic_name=topic_name, max_score=max_score, score=score)
        for (topic_name, max_score, score) in topic_scores_raw
    ]


async def select_initial_question_from_topic(
    topic: str, session_id
) -> Union[Question, None]:
    # This query makes sure an hallucinated topic is replaced by a random topic.
    query = f"""
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
    AND {QUESTION_FILTER}
ORDER BY preferred_question_order
LIMIT 1
"""
    logger.info(f"select_initial_question_from_topic: {query}")
    parameter_map = {"topic": topic, "session_id": session_id}
    questions: list = await select_from(query, parameter_map)
    if len(questions) > 0:
        (id, question, score, topic_id, topic_name, topic_description, _) = questions[0]
        topic = Topic(id=topic_id, name=topic_name, description=topic_description)
        question = Question(id=id, question=question, score=score, topic=topic)
        return question
    else:
        return None


async def save_question(question: Question) -> Question:
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO TB_QUESTION (QUESTION, SCORE, TOPIC_ID, PREFERRED_QUESTION_ORDER, YES_NO_QUESTION, SCORED)
VALUES (%(question)s, %(score)s, (SELECT ID FROM TB_TOPIC WHERE NAME = %(topic_name)s), %(preferred_question_order)s, false, true) RETURNING ID;
            """,
            {
                "question": question.question,
                "score": question.score,
                "topic_name": question.topic.name,
                "preferred_question_order": question.preferred_order,
            },
        )
        created_id = (await cur.fetchone())[0]
        return Question(
            id=created_id,
            question=question.question,
            topic=question.topic,
            score=question.score,
        )

    return await create_cursor(process_save, True)


async def update_yes_no_question(question: Question):
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
UPDATE TB_QUESTION
SET YES_NO_QUESTION = %(yes_no_question)s
WHERE ID = %(id)s
            """,
            {"yes_no_question": question.yes_no_question, "id": question.id},
        )

    await create_cursor(process_save, True)


async def save_questionnaire_status(
    questionnaire_status: QuestionnaireStatus,
) -> Union[QuestionnaireStatus, None]:
    async def process_save(cur: AsyncCursor):
        if questionnaire_status.id is None:
            await cur.execute(
                """
INSERT INTO PUBLIC.TB_QUESTIONNAIRE_STATUS(SESSION_ID, TOPIC, QUESTION, ANSWER, SCORE, SENTIMENT_ID)
SELECT CAST(%(session_id)s AS VARCHAR),
	CAST(%(topic)s AS VARCHAR),
	CAST(%(question)s AS VARCHAR),
	%(answer)s,
	%(score)s,
	(SELECT ID
		FROM TB_SENTIMENT_SCORE
		WHERE NAME = %(sentiment)s)
WHERE NOT EXISTS
		(SELECT *
			FROM TB_QUESTIONNAIRE_STATUS
			WHERE SESSION_ID = %(session_id)s
				AND TOPIC = %(topic)s
				AND QUESTION = %(question)s ) RETURNING ID
                """,
                {
                    "session_id": questionnaire_status.session_id,
                    "topic": questionnaire_status.topic,
                    "question": questionnaire_status.question,
                    "answer": questionnaire_status.answer,
                    "score": questionnaire_status.score,
                    "sentiment": questionnaire_status.sentiment,
                },
            )
        else:
            await cur.execute(
                """
UPDATE PUBLIC.TB_QUESTIONNAIRE_STATUS
SET SESSION_ID = %(session_id)s,
	TOPIC = CAST(%(topic)s AS VARCHAR),
	QUESTION = CAST(%(question)s AS VARCHAR),
	ANSWER = %(answer)s,
	SCORE = (
        SELECT SCORE from (
            SELECT CASE
                WHEN STRPOS(%(sentiment)s, 'positive') > 0 THEN SCORE.AFFIRMATIVE_SCORE
                WHEN STRPOS(%(sentiment)s, 'negative') > 0 THEN SCORE.NEGATIVE_SCORE
                WHEN STRPOS(%(sentiment)s, 'undecided') > 0 THEN SCORE.UNDECIDED_SCORE
                ELSE 0
            END SCORE
            FROM PUBLIC.TB_QUESTION_SCORE SCORE
                INNER JOIN TB_QUESTION Q ON Q.ID = SCORE.QUESTION_ID
                INNER JOIN TB_TOPIC T ON T.ID = Q.TOPIC_ID
                WHERE Q.QUESTION = CAST(%(question)s AS VARCHAR) AND T.NAME = CAST(%(topic)s AS VARCHAR)
        ) AS q1
        UNION ALL (SELECT 0) OFFSET 0 LIMIT 1
    ),
	SENTIMENT_ID =
	(SELECT ID
		FROM TB_SENTIMENT_SCORE
		WHERE NAME = %(sentiment)s),
	UPDATED_AT = NOW()
WHERE ID = %(id)s RETURNING ID
                """,
                {
                    "session_id": questionnaire_status.session_id,
                    "topic": questionnaire_status.topic,
                    "question": questionnaire_status.question,
                    "answer": questionnaire_status.answer,
                    "id": questionnaire_status.id,
                    "sentiment": questionnaire_status.sentiment,
                },
            )
        result = await cur.fetchone()
        if result is not None and len(result) > 0:
            created_id = result[0]
            return QuestionnaireStatus(
                id=created_id,
                question=questionnaire_status.question,
                answer=questionnaire_status.answer,
                topic=questionnaire_status.topic,
                score=questionnaire_status.score,
                session_id=questionnaire_status.session_id,
                topic_count=questionnaire_status.topic_count,
            )
        else:
            return None

    return await create_cursor(process_save, True)


async def select_questionnaire_counts(session_id: str) -> QuestionnaireCounts:
    query = """
SELECT S.TOPIC,

	(SELECT COUNT(DISTINCT(S1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S1
		WHERE S1.TOPIC = S.TOPIC
            AND SESSION_ID = %(session_id)s) QUESTION_COUNT,
	(SELECT QM.QUESTION_COUNT
		FROM PUBLIC.TB_QUIZ_MODE QM
		INNER JOIN PUBLIC.TB_SELECTED_QUIZ_MODE SQM ON QM.ID = SQM.QUIZ_MODE_ID
		WHERE SQM.SESSION_ID = %(session_id)s) QUESTION_TOTAL,

	(SELECT COUNT(*)
		FROM TB_TOPIC TF
		WHERE TF.NAME IN
				(SELECT SF.TOPIC
					FROM PUBLIC.TB_QUESTIONNAIRE_STATUS SF
					INNER JOIN TB_TOPIC TF1 ON TF1.NAME = SF.TOPIC
					WHERE SF.ANSWER IS NOT NULL
						AND SESSION_ID = %(session_id)s
					GROUP BY SF.TOPIC,
						TF1.QUESTION_AMOUNT
					HAVING COUNT(*) = TF1.QUESTION_AMOUNT)) FINISHED_TOPIC_COUNT,

	(SELECT COUNT(*)
		FROM PUBLIC.TB_SELECTED_TOPICS
		WHERE SESSION_ID = %(session_id)s) TOPIC_COUNT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S
INNER JOIN PUBLIC.TB_TOPIC T ON S.TOPIC = T.NAME
WHERE SESSION_ID = %(session_id)s
ORDER BY S.ID DESC
LIMIT 1
"""
    parameter_map = {"session_id": session_id}
    counts: list = await select_from(query, parameter_map)
    if len(counts) > 0:
        (
            topic,
            question_count,
            question_total,
            finished_topic_count,
            topic_total,
        ) = counts[0]
        return QuestionnaireCounts(
            topic=topic,
            question_count=question_count,
            question_total=question_total,
            finished_topic_count=finished_topic_count,
            topic_total=topic_total,
        )
    else:
        return QuestionnaireCounts(
            topic="",
            question_count=0,
            question_total=0,
            finished_topic_count=0,
            topic_total=0,
        )


async def select_remaining_topics(session_id: str) -> Union[List[str], None]:
    query = """
SELECT T.NAME
FROM TB_TOPIC T
INNER JOIN public.tb_selected_topics ST on ST.topic_id = T.id
WHERE NOT EXISTS
    (SELECT S.TOPIC
        FROM TB_QUESTIONNAIRE_STATUS S
        WHERE SESSION_ID = %(session_id)s
            AND S.ANSWER IS NOT NULL
            AND T.NAME = S.TOPIC
        GROUP BY S.TOPIC)
	AND ST.SESSION_ID = %(session_id)s"""
    parameter_map = {"session_id": session_id}
    return await handle_select_remaining(query, parameter_map)


async def handle_select_remaining(
    query: str, parameter_map: dict
) -> Union[List[str], None]:
    remaining_questions: list = await select_from(query, parameter_map)
    return [t[0] for t in remaining_questions]


async def calculate_simple_total_score(session_id: str) -> TotalScore:
    query = """
SELECT TOTAL_SCORE, MAX_SCORE, TOTAL_SCORE * 1.0 / MAX_SCORE * 100 PCT_SCORE 
FROM
	(SELECT SUM(QS.SCORE) TOTAL_SCORE,
		SUM(CASE WHEN Q.SCORED = TRUE THEN 10 ELSE 0 END) MAX_SCORE
	FROM PUBLIC.TB_QUESTIONNAIRE_STATUS QS
	INNER JOIN TB_TOPIC T ON T.NAME = QS.TOPIC
	INNER JOIN TB_QUESTION Q ON Q.QUESTION = QS.QUESTION
	WHERE SESSION_ID = %(session_id)s)
"""
    parameter_map = {"session_id": session_id}
    scoring: list = await select_from(query, parameter_map)
    if len(scoring) > 0:
        (total_score, max_score, pct_score) = scoring[0]
        return TotalScore(
            total_score=total_score, max_score=max_score, pct_score=pct_score
        )
    return TotalScore(total_score=0, max_score=0, pct_score=0.0)


async def update_questionnaire_status_score(questionnaire_status: QuestionnaireStatus):
    async def process_save(cur: AsyncCursor):
        await cur.execute(
            """
UPDATE PUBLIC.TB_QUESTIONNAIRE_STATUS
SET SCORE = %(score)s, ANSWER = %(answer)s, UPDATED_AT = NOW()
WHERE ID = %(id)s
""",
            {
                "id": questionnaire_status.id,
                "score": questionnaire_status.score,
                "answer": questionnaire_status.answer,
            },
        )
        return None

    await create_cursor(process_save, True)


async def score_on_suggested_response(question_id: int, answer: str) -> Optional[int]:
    query = """
SELECT SCORE
FROM TB_SUGGESTED_RESPONSE
WHERE QUESTION_ID = %(question_id)s
	AND BODY = %(answer)s
"""
    parameter_map = {"question_id": question_id, "answer": answer}
    scoring: list = await select_from(query, parameter_map)
    if scoring is not None and len(scoring) > 0:
        return scoring[0][0]
    return None


async def fetch_all_suggestions(question_id: int) -> List[str]:
    query = """
SELECT BODY
FROM TB_SUGGESTED_RESPONSE
WHERE QUESTION_ID = %(question_id)s
"""
    parameter_map = {"question_id": question_id}
    suggestions: list = await select_from(query, parameter_map)
    return [s[0] for s in suggestions]


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
WHERE SESSION_ID = %(session_id)s AND ANSWER IS NOT NULL and TOPIC_NAME IS NOT NULL ORDER BY UPDATED_AT
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


async def select_session_qa(session_id: str) -> List[QAScored]:
    query = """
select topic, question, answer, score from public.tb_questionnaire_status 
where SESSION_ID = %(session_id)s order by created_at
"""
    parameter_map = {"session_id": session_id}
    report_list: list = await select_from(query, parameter_map)
    return [
        QAScored(topic=topic, question=question, answer=answer, score=score)
        for (topic, question, answer, score) in report_list
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
WHERE Q.QUESTION = %(question)s AND T.NAME = %(topic)s order by S.TITLE desc
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


async def find_question(question: str, topic: str) -> Union[Question, None]:
    query = """
SELECT Q.ID, Q.QUESTION, Q.SCORE, Q.TOPIC_ID, Q.PREFERRED_QUESTION_ORDER, Q.YES_NO_QUESTION, Q.SCORED, T.NAME topic_name, T.DESCRIPTION topic_description
FROM TB_QUESTION Q
INNER JOIN TB_TOPIC T ON T.ID = Q.TOPIC_ID
WHERE T.NAME = %(topic)s
	AND QUESTION = %(question)s;
"""
    parameter_map = {"question": question, "topic": topic}
    response_list: list = await select_from(query, parameter_map)
    if len(response_list) == 0:
        return None
    (
        id,
        question,
        score,
        topic_id,
        preferred_question_order,
        yes_no_question,
        scored,
        topic_name,
        topic_description,
    ) = response_list[0]
    topic = Topic(id=topic_id, name=topic_name, description=topic_description)
    return Question(
        id=id,
        question=question,
        score=score,
        topic=topic,
        preferred_order=preferred_question_order,
        yes_no_question=yes_no_question,
        scored=scored,
    )


async def has_selected_topics(session_id: str) -> bool:
    query = """SELECT COUNT(*) FROM PUBLIC.TB_SELECTED_TOPICS WHERE SESSION_ID = %(session_id)s"""
    parameter_map = {"session_id": session_id}
    response = await select_from(query, parameter_map)
    return response[0][0] > 0


async def insert_selected_configuration(configuration: SelectedConfiguration):
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
            await cur.execute(
                query_quiz_mode,
                {"session_id": session_id, "quiz_mode_name": quiz_mode_name},
            )
            await conn.commit()

    await execute_on_connection(process_selected_topics)


async def select_quiz_modes() -> List[QuizzMode]:
    query = """select id, name, question_count from tb_quiz_mode"""
    response = await select_from(query, {})
    return [QuizzMode(id=r[0], name=r[1], question_count=r[2]) for r in response]


async def select_config_parameters() -> List[dict]:
    query = "select config_key, config_value from tb_configuration"
    config_rows = await select_from(query, {})
    return {r[0]: r[1] for r in config_rows}


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
        selected_configuration = SelectedConfiguration(
            session_id=dummy_session_id,
            quiz_mode_name=quiz_mode_name,
            topic_list=topics,
        )
        await insert_selected_configuration(selected_configuration)

    async def test_quizz_modes():
        quizz_modes = await select_quiz_modes()
        assert quizz_modes is not None
        for quizz_mode in quizz_modes:
            print(quizz_mode.model_dump_json())

    async def test_save_questionnaire_status():
        from data_assessment_agent.test.provider.questionnaire_status_provider import (
            create_questionnaire_status,
        )

        questionnaire_status = create_questionnaire_status()
        new_questionnaire_status = await save_questionnaire_status(questionnaire_status)
        assert new_questionnaire_status is not None
        print(new_questionnaire_status.id)

    async def test_select_initial_question():
        initial_question = await select_initial_question("dummy")
        print(initial_question)
        assert initial_question is None

    async def test_select_questionnaire_counts():
        questionnaire_counts = await select_questionnaire_counts(
            "dcbfafc8-2741-46ec-ac40-34d72b491747"
        )
        print(questionnaire_counts)

    async def test_select_remaining_topics():
        remaining_topics = await select_remaining_topics(
            "dcbfafc8-2741-46ec-ac40-34d72b491747"
        )
        print(remaining_topics)

    async def test_find_question():
        yes_no_question = await find_question(
            "What are the organization's short-term and long-term business goals?",
            "Business Alignment",
        )
        print(yes_no_question)

    async def test_score_on_suggested_response():
        score = await score_on_suggested_response(
            458,
            "The data transformations and computations are relatively straightforward, involving basic operations such as sorting, filtering, and simple arithmetic calculations. This level of complexity is suitable for tasks that require minimal data manipulation.",
        )
        print(score)

    async def test_fetch_all_suggestions():
        suggestions = await fetch_all_suggestions(458)
        for s in suggestions:
            print(s)

    async def test_update_questionnaire_status_score():
        question = await select_random_question()
        assert question is not None
        questionnaire_status = QuestionnaireStatus(
            session_id="dummy",
            topic=question.topic.name,
            question=question.question,
            answer="Dummy answer",
        )
        questionnaire_status_saved = await save_questionnaire_status(
            questionnaire_status
        )
        assert questionnaire_status_saved.id is not None
        await update_questionnaire_status_score(questionnaire_status_saved.id, 5)

    async def test_select_remaining_questions():
        remaining = await select_remaining_questions(
            "7562def8-24ed-4756-83b2-1ec124ae4baf", "Business Alignment"
        )
        for r in remaining:
            print(r)

    async def test_select_answered_questions_in_topic():
        remaining = await select_answered_questions_in_topic(
            "7562def8-24ed-4756-83b2-1ec124ae4baf", "Business Alignment"
        )
        for r in remaining:
            print(r)

    async def test_select_answered_questions_in_session():
        answered = await select_answered_questions_in_session(
            "7562def8-24ed-4756-83b2-1ec124ae4baf"
        )
        for r in answered:
            print(r)

    # asyncio.run(test_select_topic_scores())
    # asyncio.run(test_select_question_scores())
    # asyncio.run(test_select_suggestions())
    # asyncio.run(test_select_topics())
    # asyncio.run(test_has_selected_topics())
    # asyncio.run(test_insert_into_selected_topics())
    # asyncio.run(test_quizz_modes())
    # asyncio.run(test_save_questionnaire_status())
    # asyncio.run(test_select_initial_question())
    # asyncio.run(test_select_questionnaire_counts())
    # asyncio.run(test_select_remaining_topics())
    # asyncio.run(test_find_question())
    # asyncio.run(test_fetch_all_suggestions())
    # asyncio.run(test_select_remaining_questions())
    # asyncio.run(test_select_answered_questions_in_topic())
    asyncio.run(test_select_answered_questions_in_session())
