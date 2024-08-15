import unittest

from data_assessment_agent.service.maturity_level_service import create_user_message
from data_assessment_agent.test.provider.maturity_level_provider import (
    provide_session_report,
)


class TestDateUtils(unittest.TestCase):
    def test_create_user_message(self):
        session_output = provide_session_report()
        user_message = create_user_message(session_output)
        assert user_message is not None
        assert user_message.find(session_output) > 1
