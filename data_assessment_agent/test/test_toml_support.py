import unittest

from data_assessment_agent.config.toml_support import prompts


class TestConfig(unittest.TestCase):
    def test_toml_support(self):
        assert prompts is not None
        assert prompts["ranking"] is not None
        assert prompts["ranking"]["user_message"] is not None
        assert prompts["ranking"]["system_message"] is not None


if __name__ == "__main__":
    unittest.main()
