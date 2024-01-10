from typing import List
from collections import defaultdict

from data_assessment_agent.service.persistence_service import load_questions
from data_assessment_agent.service.ranking_service_vector import (
    lance_db_questions_db,
    query_for_topic,
)
from data_assessment_agent.model.vector_db_model import Questions


def index_questions():
    questions = load_questions()
    d = defaultdict(list)
    for q in questions:
        d[q.topic.name].append(q.question)
    for k, v in d.items():
        lance_db_questions_db.drop_table(k)
        table = lance_db_questions_db.create_table(k, schema=Questions)
        question_dict = [{"question": question} for question in v]
        table.add(question_dict)


if __name__ == "__main__":
    index_questions()
    res = query_for_topic("Advanced Analytics", "What tools do you use?")
    for r in res:
        print(r)
