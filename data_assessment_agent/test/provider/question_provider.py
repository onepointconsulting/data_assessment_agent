from data_assessment_agent.model.db_model import Question
from data_assessment_agent.test.provider.topic_provider import create_dummy_topic


def create_dummy_question() -> Question:
    topic = create_dummy_topic()
    return Question(question="What is a dummy?", score=10, topic=topic)


def create_question_answers() -> str:
    question = "What best describes the reality of your organization's advanced analytics tools landscape?"
    answer = "Our advanced analytics tools landscape includes a data lake based on Snowflake which hosts the data used by our Power BI reports. We are currently not using any advanced features of Power BI related to machine learning. Power BI is in this context only a visualization instrument."
    return f"""{question}
{answer}"""
