from data_assessment_agent.model.db_model import Question
from data_assessment_agent.test.provider.topic_provider import create_dummy_topic


def create_dummy_question():
    topic = create_dummy_topic()
    return Question(question="What is a dummy?", score=10, topic=topic)
