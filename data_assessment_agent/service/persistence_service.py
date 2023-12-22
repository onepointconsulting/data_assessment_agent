from typing import Callable, Any

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from data_assessment_agent.config.config import db_cfg
from data_assessment_agent.model.db_model import Topic, Question


def connect_to_db() -> connection:
    conn = psycopg2.connect(
        f"dbname={db_cfg.db_name} user={db_cfg.db_user} password={db_cfg.db_password} host={db_cfg.db_host} port={db_cfg.db_port}"
    )
    return conn


def create_cursor(func: Callable) -> Any:
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            return func(cur)


def select_topic(topic: Topic):
    def handle_select_topics(cur: cursor):
        cur.execute("SELECT id, name, description FROM tb_topic")
        many_rows = cur.fetchall()
        return list(many_rows)

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
            INSERT INTO tb_topic (name, description)
            VALUES (%(name)s, %(description)s) RETURNING id;
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
        question.id = created_id
        return created_id

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


if __name__ == "__main__":
    from data_assessment_agent.test.provider import topic_provider, question_provider

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
