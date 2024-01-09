from typing import List
from collections import defaultdict

import lancedb
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector
from data_assessment_agent.service.persistence_service import load_questions
from data_assessment_agent.config.config import cfg

registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get("openai").create()


class Questions(LanceModel):
    question: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()


def connect_to_lance_questions():
    db_file = cfg.lance_db_questions
    db = lancedb.connect(db_file)
    return db


lance_db_questions_db = connect_to_lance_questions()


def query_for_topic(topic: str, question: str, limit=5) -> List[str]:
    table = lance_db_questions_db.open_table(topic)
    results = table.search(question).limit(limit).to_pydantic(Questions)
    return [r.question for r in results]


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
    res = query_for_topic("Advanced Analytics", "What tools do you use?")
    for r in res:
        print(r)
