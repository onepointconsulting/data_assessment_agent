import unittest

from data_assessment_agent.config.config import cfg


class TestConfig(unittest.TestCase):
    def test_config(self):
        assert cfg is not None
        assert cfg.openai_timeout > 0.0
        assert cfg.open_ai_client is not None
        assert cfg.project_root.exists()


if __name__ == "__main__":
    unittest.main()
