import unittest

from data_assessment_agent.model.sentiment import AnswerSentiment, Sentiment


class TestDBModel(unittest.TestCase):
    def test_sentiment_response(self):
        sentiment_response = AnswerSentiment(sentiment=Sentiment.AMBIGUOUS)
        json = sentiment_response.model_json_schema()
        assert json is not None
        print("sentiment_response model", json)


if __name__ == "__main__":
    unittest.main()
