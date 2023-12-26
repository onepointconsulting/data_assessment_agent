import unittest

from data_assessment_agent.model.transport import ServerMessage


class TestDBModel(unittest.TestCase):
    def test_topic(self):
        server_message = ServerMessage(
            response="This is a response", sources=None, sessionId="12312312321"
        )
        json_schema = server_message.model_dump_json()
        assert json_schema is not None
        assert "sessionId" in str(json_schema)
        print(json_schema)


if __name__ == "__main__":
    unittest.main()
