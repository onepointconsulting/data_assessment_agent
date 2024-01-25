import unittest

from data_assessment_agent.service.chart.spider_chart import (
    generate_spider_chart,
)
from data_assessment_agent.test.provider.topic_score_provider import create_topic_scores
from data_assessment_agent.model.db_model import TopicScoreResult


class TestDBModel(unittest.TestCase):
    def test_generate_spider_chart(self):
        topic_scores = create_topic_scores()
        assert topic_scores is not None
        assert isinstance(topic_scores, TopicScoreResult)
        spider_chart = generate_spider_chart(topic_score_result=topic_scores, size=12)
        assert spider_chart is not None
        assert spider_chart.exists()


if __name__ == "__main__":
    unittest.main()
