## Abandoned approach by Sasha

from typing import List

import lancedb
from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.vector_db_model import Questions


def connect_to_lance_questions():
    db_file = cfg.lance_db_questions
    db = lancedb.connect(db_file)
    return db


lance_db_questions_db = connect_to_lance_questions()


def query_for_topic(topic: str, question: str, limit=5) -> List[str]:
    table = lance_db_questions_db.open_table(topic)
    results = table.search(question).limit(limit).to_pydantic(Questions)
    return [r.question for r in results]


async def rank_questions(
    topic: str, question_answers: str, ranking_questions: List[str]
) -> List[str]:
    res = query_for_topic(topic, question_answers, limit=len(ranking_questions + 5))
    return [r for r in res if r in ranking_questions]


if __name__ == "__main__":
    from data_assessment_agent.test.provider.question_provider import (
        create_question_answers,
    )

    question_answers = create_question_answers()
    assert isinstance(question_answers, str)
