import unittest

from data_assessment_agent.model.ranking import RankedQuestionsResponse


class TestConfig(unittest.TestCase):
    def test_model_ranking(self):
        schema = RankedQuestionsResponse.model_json_schema()
        assert schema is not None
        assert schema.get("properties") is not None
        assert schema.get("properties").get("ranked_questions") is not None
        assert schema.get("properties").get("ranked_questions").get("type") == "array"
        print(schema)


if __name__ == "__main__":
    unittest.main()
