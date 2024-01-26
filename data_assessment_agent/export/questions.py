import pandas as pd

from data_assessment_agent.config.config import cfg
from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.service.persistence_service import load_questions

if __name__ == "__main__":
    logger.info("Getting all questions")
    questions = load_questions()
    data = []
    for question in questions:
        data.append(
            [
                question.id,
                question.question,
                question.topic.name,
                question.yes_no_question,
                question.scored,
            ]
        )
    df = pd.DataFrame(data, columns=["id", "question", "topic", "yes no", "scored"])
    df.to_csv(cfg.exports_tmp_folder / "questions.csv")
