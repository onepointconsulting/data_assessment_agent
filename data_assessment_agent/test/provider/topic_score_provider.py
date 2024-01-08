from data_assessment_agent.model.db_model import TopicScore, TopicScoreResult


def create_topic_scores() -> TopicScoreResult:
    session_id = "b8ce68f0-f754-4af8-8822-97dac817250d"
    topic_scores = [
        TopicScore(topic_name="Advanced Analytics", max_score=50, score=40),
        TopicScore(topic_name="Business Alignment", max_score=50, score=40),
        TopicScore(topic_name="Data Acquisition", max_score=50, score=40),
        TopicScore(topic_name="Data Architecture", max_score=50, score=30),
        TopicScore(topic_name="Data Assets", max_score=50, score=45),
        TopicScore(topic_name="Data Governance", max_score=50, score=35),
        TopicScore(topic_name="Data Modelling", max_score=50, score=50),
        TopicScore(topic_name="Data Quality", max_score=50, score=40),
        TopicScore(topic_name="Data Security", max_score=50, score=30),
        TopicScore(topic_name="Dataops", max_score=50, score=30),
        TopicScore(topic_name="Infrastructure", max_score=50, score=30),
        TopicScore(topic_name="Reporting", max_score=50, score=50),
        TopicScore(topic_name="Testing", max_score=50, score=40),
    ]
    return TopicScoreResult(session_id=session_id, topic_scores=topic_scores)
