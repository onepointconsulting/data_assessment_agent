from typing import Callable, Any, List, Union

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from data_assessment_agent.config.config import db_cfg
from data_assessment_agent.model.db_model import (
    DbSuggestedResponse,
    Topic,
    Question,
    QuestionnaireStatus,
    QuestionnaireCounts,
    SessionReport,
)
from data_assessment_agent.model.assessment_framework import SuggestedResponse


def connect_to_db() -> connection:
    conn = psycopg2.connect(
        f"dbname={db_cfg.db_name} user={db_cfg.db_user} password={db_cfg.db_password} host={db_cfg.db_host} port={db_cfg.db_port}"
    )
    return conn


def create_cursor(func: Callable) -> Any:
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            return func(cur)


def handle_select_func(query: str, query_params: dict):
    def func(cur: cursor):
        cur.execute(
            query,
            query_params,
        )
        return list(cur.fetchall())

    return func


def select_topic(topic: Topic):
    def handle_select_topics(cur: cursor):
        cur.execute(
            "SELECT id, name, description FROM tb_topic where name = %(name)s",
            {"name": topic.name},
        )
        return list(cur.fetchall())

    return create_cursor(handle_select_topics)


def delete_topic(topic: Topic):
    create_cursor(
        lambda cur: cur.execute(
            """
            DELETE FROM tb_topic
            where name = %(name)s;
            """,
            {"name": topic.name},
        )
    )


def save_topic(topic: Topic) -> Topic:
    def process_save(cur: cursor):
        cur.execute(
            """
INSERT INTO TB_TOPIC (NAME, DESCRIPTION, QUESTION_AMOUNT, PREFERRED_TOPIC_ORDER)
VALUES (%(name)s, %(description)s, 5, %(preferred_topic_order)s) RETURNING ID;
            """,
            {
                "name": topic.name,
                "description": topic.description,
                "preferred_topic_order": topic.preferred_topic_order,
            },
        )
        created_id = cur.fetchone()[0]
        topic.id = created_id
        return topic

    return create_cursor(process_save)


def save_question(question: Question) -> Question:
    def process_save(cur: cursor):
        cur.execute(
            """
INSERT INTO TB_QUESTION (QUESTION, SCORE, TOPIC_ID, PREFERRED_QUESTION_ORDER)
VALUES (%(question)s, %(score)s, (SELECT ID FROM TB_TOPIC WHERE NAME = %(topic_name)s), %(preferred_question_order)s) RETURNING ID;
            """,
            {
                "question": question.question,
                "score": question.score,
                "topic_name": question.topic.name,
                "preferred_question_order": question.preferred_order,
            },
        )
        created_id = cur.fetchone()[0]
        return Question(
            id=created_id,
            question=question.question,
            topic=question.topic,
            score=question.score,
        )

    return create_cursor(process_save)


def save_suggested_response(
    suggested_response: DbSuggestedResponse,
) -> DbSuggestedResponse:
    assert (
        suggested_response.question.id is not None
    ), "There is no question id. Make sure it exists to store the suggestion"

    def process_save(cur: cursor):
        cur.execute(
            """
INSERT INTO PUBLIC.TB_SUGGESTED_RESPONSE(TITLE, SUBTITLE, BODY, QUESTION_ID)
VALUES(%(title)s, %(subtitle)s, %(body)s, %(question_id)s) RETURNING ID
            """,
            {
                "title": suggested_response.title,
                "subtitle": suggested_response.subtitle,
                "body": suggested_response.body,
                "question_id": suggested_response.question.id,
            },
        )
        copy = suggested_response.model_copy()
        copy.id = cur.fetchone()[0]
        return copy

    return create_cursor(process_save)


def delete_question(question: Question):
    create_cursor(
        lambda cur: cur.execute(
            """
            DELETE FROM tb_question
            where id = %(id)s;
            """,
            {"id": question.id},
        )
    )


def suggestion_exists_for(question: Question):
    question_str = question.question
    topic = question.topic.name

    def handle_select(cur: cursor):
        cur.execute(
            """
SELECT COUNT(*) FROM TB_SUGGESTED_RESPONSE S
INNER JOIN TB_QUESTION Q ON Q.ID = S.QUESTION_ID
INNER JOIN TB_TOPIC T ON T.ID = Q.TOPIC_ID
WHERE Q.QUESTION = %(question)s
	AND T.NAME = %(topic)s""",
            {"question": question_str, "topic": topic},
        )
        return list(cur.fetchall())
    counts = create_cursor(handle_select)
    return counts[0][0] > 0


def delete_suggested_response(id: int):
    create_cursor(
        lambda cur: cur.execute(
            """
                DELETE FROM TB_SUGGESTED_RESPONSE
                where id = %(id)s;
                """,
            {"id": id},
        )
    )


def clear_suggested_responses():
    create_cursor(
        lambda cur: cur.execute(
            """
                TRUNCATE TABLE TB_SUGGESTED_RESPONSE;
                """,
            {"id": id},
        )
    )


def load_questions() -> List[Question]:
    def handle_select(cur: cursor):
        cur.execute(
            """
SELECT Q.ID,
	Q.QUESTION,
	Q.SCORE,
	T.ID TOPIC_ID,
	T.NAME TOPIC_NAME,
	T.DESCRIPTION TOPIC_DESCRIPTION,
    T.QUESTION_AMOUNT
FROM TB_QUESTION Q
INNER JOIN TB_TOPIC T ON Q.TOPIC_ID = T.ID
ORDER BY T.PREFERRED_TOPIC_ORDER, Q.ID"""
        )
        return list(cur.fetchall())

    questions: list = create_cursor(handle_select)
    final_questions = []
    for (
        id,
        question,
        score,
        topic_id,
        topic_name,
        topic_description,
        question_amount,
    ) in questions:
        topic = Topic(
            id=topic_id,
            name=topic_name,
            description=topic_description,
            question_amount=question_amount,
        )
        final_questions.append(
            Question(id=id, question=question, score=score, topic=topic)
        )
    return final_questions


def save_questionnaire_status(
    questionnaire_status: QuestionnaireStatus,
) -> Union[QuestionnaireStatus, None]:
    def process_save(cur: cursor):
        if questionnaire_status.id is None:
            cur.execute(
                """
INSERT INTO PUBLIC.TB_QUESTIONNAIRE_STATUS(SESSION_ID, TOPIC, QUESTION, ANSWER, SCORE, SENTIMENT_ID)
SELECT %(session_id)s,
	%(topic)s,
	%(question)s,
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
            cur.execute(
                """
    update public.tb_questionnaire_status set session_id = %(session_id)s, topic = %(topic)s, 
        question = %(question)s, answer = %(answer)s, score = %(score)s, sentiment_id = (select id from tb_sentiment_score where name = %(sentiment)s),
        updated_at = NOW()
    where id = %(id)s returning id
                """,
                {
                    "session_id": questionnaire_status.session_id,
                    "topic": questionnaire_status.topic,
                    "question": questionnaire_status.question,
                    "answer": questionnaire_status.answer,
                    "score": questionnaire_status.score,
                    "id": questionnaire_status.id,
                    "sentiment": questionnaire_status.sentiment,
                },
            )
        result = cur.fetchone()
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

    return create_cursor(process_save)


def select_last_question(session_id: str) -> Union[QuestionnaireStatus, None]:
    def handle_select(cur: cursor):
        cur.execute(
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
        return list(cur.fetchall())

    statuses: list = create_cursor(handle_select)
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


def select_remaining_questions(session_id: str, topic: str) -> Union[List[str], None]:
    query = """
SELECT Q.QUESTION
FROM PUBLIC.TB_QUESTION Q
INNER JOIN PUBLIC.TB_TOPIC T ON Q.TOPIC_ID = T.ID
WHERE T.NAME = %(topic)s
	AND NOT EXISTS
		(SELECT QUESTION
			FROM PUBLIC.TB_QUESTIONNAIRE_STATUS
			WHERE SESSION_ID = %(session_id)s
				AND Q.QUESTION = QUESTION
				AND TOPIC = %(topic)s
                AND ANSWER IS NOT NULL
			GROUP BY QUESTION)"""
    parameter_map = {"session_id": session_id, "topic": topic}
    return handle_select_remaining(query, parameter_map)


def select_remaining_topics(session_id: str) -> Union[List[str], None]:
    query = """
SELECT T.NAME
FROM TB_TOPIC T
WHERE NOT EXISTS
    (SELECT S.TOPIC
        FROM TB_QUESTIONNAIRE_STATUS S
        WHERE SESSION_ID = %(session_id)s
            AND S.ANSWER IS NOT NULL
            AND T.NAME = S.TOPIC
        GROUP BY S.TOPIC)"""
    parameter_map = {"session_id": session_id}
    return handle_select_remaining(query, parameter_map)


def handle_select_remaining(query: str, parameter_map: dict) -> Union[List[str], None]:
    handle_select = handle_select_func(query, parameter_map)
    remaining_questions: list = create_cursor(handle_select)
    return [t[0] for t in remaining_questions]


def select_answered_questions_in_topic(
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
    return handle_question_answers_select(query, parameter_map)


def select_answered_questions_in_session(session_id: str) -> Union[List[str], None]:
    query = """
SELECT S.QUESTION,
	S.ANSWER
FROM TB_QUESTIONNAIRE_STATUS S
WHERE SESSION_ID = %(session_id)s
	AND S.ANSWER IS NOT NULL
ORDER BY S.ID"""
    parameter_map = {"session_id": session_id}
    return handle_question_answers_select(query, parameter_map)


def handle_question_answers_select(
    query: str, parameter_map: dict
) -> Union[List[str], None]:
    handle_select = handle_select_func(query, parameter_map)
    answered_questions: list = create_cursor(handle_select)
    return [f"{t[0]}\n{t[1]}" for t in answered_questions]


def select_last_empty_question(session_id: str) -> Union[QuestionnaireStatus, None]:
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
    handle_select = handle_select_func(query, parameter_map)
    unanswered_questions: list = create_cursor(handle_select)
    if len(unanswered_questions) > 0:
        (id, session_id, topic, question, created_at) = unanswered_questions[0]
        return QuestionnaireStatus(
            id=id, session_id=session_id, topic=topic, question=question
        )
    else:
        return None


def select_initial_question_from_topic(topic: str) -> Union[Question, None]:
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
WHERE T.NAME = %(topic)s
ORDER BY preferred_question_order
LIMIT 1
"""
    parameter_map = {"topic": topic}
    handle_select = handle_select_func(query, parameter_map)
    questions: list = create_cursor(handle_select)
    if len(questions) > 0:
        (id, question, score, topic_id, topic_name, topic_description, _) = questions[0]
        topic = Topic(id=topic_id, name=topic_name, description=topic_description)
        question = Question(id=id, question=question, score=score, topic=topic)
        return question
    else:
        return None


def select_questionnaire_counts(session_id: str) -> QuestionnaireCounts:
    query = """
SELECT S.TOPIC,

	(SELECT COUNT(DISTINCT(S1.QUESTION))
		FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S1
		WHERE S1.TOPIC = S.TOPIC
            AND SESSION_ID = %(session_id)s) QUESTION_COUNT,
	T.QUESTION_AMOUNT QUESTION_TOTAL,

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
		FROM TB_TOPIC) TOPIC_COUNT
FROM PUBLIC.TB_QUESTIONNAIRE_STATUS S
INNER JOIN PUBLIC.TB_TOPIC T ON S.TOPIC = T.NAME
WHERE SESSION_ID = %(session_id)s
ORDER BY S.ID DESC
LIMIT 1
"""
    parameter_map = {"session_id": session_id}
    handle_select = handle_select_func(query, parameter_map)
    counts: list = create_cursor(handle_select)
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


def select_suggestions(question: str, topic: str) -> List[SuggestedResponse]:
    query = """
SELECT Q.ID, Q.QUESTION, Q.SCORE, T.ID, T.NAME, T.DESCRIPTION, S.ID, S.TITLE, S.SUBTITLE, S.BODY
FROM TB_SUGGESTED_RESPONSE S
INNER JOIN TB_QUESTION Q ON Q.ID = S.QUESTION_ID
INNER JOIN TB_TOPIC T ON T.ID = Q.TOPIC_ID
WHERE Q.QUESTION = %(question)s
	AND T.NAME = %(topic)s
"""
    parameter_map = {"question": question, "topic": topic}
    handle_select = handle_select_func(query, parameter_map)
    response_list: list = create_cursor(handle_select)
    res_list = []
    for r in response_list:
        (
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
        ) = r
        suggestion = SuggestedResponse(
            title=suggestion_title, subtitle=suggestion_subtitle, body=suggestion_body
        )
        res_list.append(suggestion)
    return res_list


def select_session_report(session_id: str) -> List[SessionReport]:
    query = """
SELECT S.TOPIC,
	S.QUESTION,
	S.ANSWER,
	S.SCORE,
	SS.NAME SENTIMENT,
    S.CREATED_AT,
    S.UPDATED_AT
FROM TB_QUESTIONNAIRE_STATUS S
INNER JOIN TB_SENTIMENT_SCORE SS ON S.SENTIMENT_ID = SS.ID
WHERE S.SESSION_ID = %(session_id)s
	AND S.ANSWER IS NOT NULL
"""
    parameter_map = {"session_id": session_id}
    handle_select = handle_select_func(query, parameter_map)
    report_list: list = create_cursor(handle_select)
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


def select_topics() -> List[str]:
    query = """
SELECT NAME
FROM TB_TOPIC
ORDER BY NAME
"""
    handle_select = handle_select_func(query, {})
    topics: list = create_cursor(handle_select)
    return [t[0] for t in topics]


if __name__ == "__main__":
    from data_assessment_agent.test.provider import topic_provider, question_provider
    from data_assessment_agent.test.provider.suggestion_provider import (
        create_suggestion_response,
    )

    def write_question_and_delete():
        topic = topic_provider.create_dummy_topic()
        assert topic is not None
        topic = save_topic(topic)
        rows = select_topic(topic)
        for r in rows:
            print(r)
        question = question_provider.create_dummy_question()
        question_id = save_question(question)
        print(question_id)
        delete_question(question)
        delete_topic(topic)

    questions = load_questions()
    first_question = questions[0]
    assert questions is not None
    last_question = select_last_question("")
    assert last_question is None
    print("== remaining questions ==")
    questions = select_remaining_questions(
        "b8ce68f0-f754-4af8-8822-97dac817250d", "Advanced Analytics"
    )
    for i, question in enumerate(questions):
        print(question)

    print("== answered_question in topic ==")
    answered_questions = select_answered_questions_in_topic(
        "b8ce68f0-f754-4af8-8822-97dac817250d", "Advanced Analytics"
    )
    for i, answered_question in enumerate(answered_questions):
        print(answered_question)

    print("== answered_question overall ==")
    answered_questions = select_answered_questions_in_session(
        "b8ce68f0-f754-4af8-8822-97dac817250d"
    )
    for i, answered_question in enumerate(answered_questions):
        print(answered_question)

    print("== Remaining topics ==")
    remaining_topics = select_remaining_topics("b8ce68f0-f754-4af8-8822-97dac817250d")
    for i, remaining_topic in enumerate(remaining_topics):
        print(remaining_topic)

    print("== Random question from topic ==")
    random_question = select_initial_question_from_topic("Advanced Analytics")
    print(random_question)

    print("=== Session Report ===")
    report_entries = select_session_report("b8ce68f0-f754-4af8-8822-97dac817250d")
    for report in report_entries:
        print(report)

    print("=== Topics ===")
    topics = select_topics()
    for topic in topics:
        print(topic)

    print("=== Save suggested response ===")
    suggestion = create_suggestion_response()
    suggestion.question = first_question
    saved_suggestion = save_suggested_response(suggestion)
    assert saved_suggestion.id is not None

    delete_suggested_response(saved_suggestion.id)

    print("=== Suggestions ===")
    suggestions = select_suggestions(
        "What are the organization's overall business goals and objectives?",
        "Business Alignment",
    )
    for s in suggestions:
        print(s)
