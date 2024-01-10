import unittest
import re

from data_assessment_agent.utils.date_utils import (
    generate_ISO_8601_timestamp,
)


class TestDateUtils(unittest.TestCase):
    def test_generate_ISO_8601_timestamp(self):
        generatd_date = generate_ISO_8601_timestamp()
        assert generatd_date is not None
        matches = re.search(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", generatd_date
        )
        assert matches is not None
