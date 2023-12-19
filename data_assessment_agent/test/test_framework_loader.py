import unittest

from data_assessment_agent.config.framework_loader import (
    import_framework,
    import_framework_objects,
)
from data_assessment_agent.model.assessment_framework import AssessmentFramework


class TestConfig(unittest.TestCase):
    def test_import_framework(self):
        framework = import_framework()
        assert framework is not None
        assert isinstance(framework, dict)

    def test_import_framework(self):
        framework = import_framework_objects()
        assert framework is not None
        assert isinstance(framework, AssessmentFramework)
        assert len(framework.categories) > 0


if __name__ == "__main__":
    unittest.main()
