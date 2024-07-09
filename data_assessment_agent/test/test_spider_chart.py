import unittest

from data_assessment_agent.service.chart.spider_chart import (
    generate_spider_chart,
)
from data_assessment_agent.test.provider.topic_score_provider import (
    create_topic_scores,
    create_topic_scores_2,
)
from data_assessment_agent.model.db_model import TopicScoreResult


class TestDBModel(unittest.TestCase):
    def test_generate_spider_chart(self):
        topic_scores = create_topic_scores()
        self.execute_test(topic_scores)

    def test_generate_spider_chart_2(self):
        topic_scores = create_topic_scores_2()
        self.execute_test(topic_scores)

    def execute_test(self, topic_scores):
        assert topic_scores is not None
        assert isinstance(topic_scores, TopicScoreResult)
        spider_chart = generate_spider_chart(topic_score_result=topic_scores, size=12)
        assert spider_chart is not None
        assert spider_chart.exists()
        print(spider_chart)


if __name__ == "__main__":
    unittest.main()
