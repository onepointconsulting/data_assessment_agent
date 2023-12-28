from typing import Callable, Any, List, Union

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from data_assessment_agent.config.config import db_cfg
from data_assessment_agent.model.db_model import Topic, Question, QuestionnaireStatus


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
            INSERT INTO tb_topic (name, description, question_amount)
            VALUES (%(name)s, %(description)s, 5) RETURNING id;
            """,
            {"name": topic.name, "description": topic.description},
        )
        created_id = cur.fetchone()[0]
        topic.id = created_id
        return topic

    return create_cursor(process_save)


def save_question(question: Question) -> Question:
    def process_save(cur: cursor):
        cur.execute(
            """
            INSERT INTO tb_question (question, score, topic_id)
            VALUES (%(question)s, %(score)s, (select id from tb_topic where name = %(topic_name)s)) RETURNING id;
            """,
            {
                "question": question.question,
                "score": question.score,
                "topic_name": question.topic.name,
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


def load_questions() -> List[Question]:
    def handle_select(cur: cursor):
        cur.execute(
            """
select q.id, q.question, q.score, t.id topic_id, t.name topic_name, t.description topic_description
from tb_question q inner join tb_topic t 
on q.topic_id = t.id 
order by id"""
        )
        return list(cur.fetchall())

    questions: list = create_cursor(handle_select)
    final_questions = []
    for id, question, score, topic_id, topic_name, topic_description in questions:
        topic = Topic(id=topic_id, name=topic_name, description=topic_description)
        final_questions.append(
            Question(id=id, question=question, score=score, topic=topic)
        )
    return final_questions


def save_questionnaire_status(
    questionnaire_status: QuestionnaireStatus,
) -> QuestionnaireStatus:
    def process_save(cur: cursor):
        cur.execute(
            """
insert into public.tb_questionnaire_status(session_id, topic, question, answer, score)
values(%(session_id)s, %(topic)s, %(question)s, %(answer)s, %(score)s) returning id
            """,
            {
                "session_id": questionnaire_status.session_id,
                "topic": questionnaire_status.topic,
                "question": questionnaire_status.question,
                "answer": questionnaire_status.answer,
                "score": questionnaire_status.score,
            },
        )
        created_id = cur.fetchone()[0]
        return QuestionnaireStatus(
            id=created_id,
            question=questionnaire_status.question,
            answer=questionnaire_status.answer,
            topic=questionnaire_status.topic,
            score=questionnaire_status.score,
            session_id=questionnaire_status.session_id,
            topic_count=questionnaire_status.topic_count,
        )

    return create_cursor(process_save)


def select_last_question(session_id: str) -> Union[QuestionnaireStatus, None]:
    def handle_select(cur: cursor):
        cur.execute(
            """
select s.id, s.session_id, s.topic, s.question, s.answer, s.score, s.created_at, 
(select count(*) from public.tb_questionnaire_status qs1 where qs1.session_id = %(session_id)s and qs1.topic = s.topic and answer is null) topic_count,
(select t.question_amount - count(*) from public.tb_questionnaire_status qs1 where qs1.session_id = %(session_id)s and qs1.topic = s.topic and answer is null) topic_missing
from public.tb_questionnaire_status s
inner join tb_topic t on t.name = s.topic 
where session_id = %(session_id)s 
order by id desc limit 1""",
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
    )


def select_remaining_questions(session_id: str, topic: str) -> Union[List[str], None]:
    query = """
select q.question from public.tb_question q 
inner join public.tb_topic t on q.topic_id = t.id
where t.name = %(topic)s and not exists(select question from public.tb_questionnaire_status
where session_id = %(session_id)s and q.question = question
and topic = %(topic)s
group by question)"""
    parameter_map = {"session_id": session_id, "topic": topic}
    handle_select = handle_select_func(query, parameter_map)
    remaining_questions: list = create_cursor(handle_select)
    return [t[0] for t in remaining_questions]


def select_answered_questions_in_topic(session_id: str, topic: str) -> Union[List[str], None]:
    query = """
select question, (select answer from tb_questionnaire_status where id = max(s.id)) from tb_questionnaire_status s
where session_id = %(session_id)s and topic = %(topic)s and answer is not null
group by question"""
    parameter_map = {"session_id": session_id, "topic": topic}
    handle_select = handle_select_func(query, parameter_map)
    answered_questions: list = create_cursor(handle_select)
    return [f"{t[0]}\n{t[1]}" for t in answered_questions]


def select_last_question(session_id: str) -> Union[List[str], None]:
    pass


if __name__ == "__main__":
    from data_assessment_agent.test.provider import topic_provider, question_provider

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
    assert questions is not None
    last_question = select_last_question("")
    assert last_question is None
    questions = select_remaining_questions('b8ce68f0-f754-4af8-8822-97dac817250d', 'Advanced Analytics')
    for i, question in enumerate(questions):
        print(question)

    print("= answered_question =")
    answered_questions = select_answered_questions_in_topic('b8ce68f0-f754-4af8-8822-97dac817250d', 'Advanced Analytics')
    for i, answered_question in enumerate(answered_questions):
        print(answered_question)
