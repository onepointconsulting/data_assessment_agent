from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.framework_loader import import_framework_objects
from data_assessment_agent.service.persistence_service import save_topic, save_question
from data_assessment_agent.model.db_model import Topic, Question

if __name__ == "__main__":
    assessment_framework = import_framework_objects()
    assert assessment_framework is not None
    for category, questions in assessment_framework.categories.items():
        topic = Topic(name=category, description=category)
        try:
            saved_topic = save_topic(topic)
            print(saved_topic)
            for question in questions:
                try:
                    db_question = Question(
                        question=question.question,
                        score=question.score,
                        topic=saved_topic,
                    )
                    save_question(db_question)
                except:
                    logger.exception("Failed to insert question")
        except:
            logger.exception("Failed to insert topic")
