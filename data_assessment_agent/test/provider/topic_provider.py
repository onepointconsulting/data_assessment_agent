from data_assessment_agent.model.db_model import Topic


def create_analytics_topic():
    return Topic(name="Advanced Analytics", description="Advanced Analytics")


def create_dummy_topic():
    return Topic(name="dummy", description="dummy")
