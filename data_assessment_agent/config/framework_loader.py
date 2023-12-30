from pathlib import Path

import yaml

from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.assessment_framework import (
    AssessmentFramework,
    Question,
)


def import_framework() -> dict:
    path: Path = cfg.framework_questionnaire_yaml
    framework_questionnaire = yaml.safe_load(path.read_text())
    return framework_questionnaire


def import_framework_objects() -> AssessmentFramework:
    framework_dict = import_framework()
    assessment_framework = AssessmentFramework(categories={}, preferred_order={})
    for category, properties in framework_dict.items():
        questions = properties.get("questions", [])
        preferred_topic_order = properties.get("preferred_topic_order", 0)
        framework_questions = [
            Question(
                category=question["category"],
                question=question["question"],
                score=question["score"],
            )
            for question in questions
        ]
        assessment_framework.categories[category] = framework_questions
        assessment_framework.preferred_order[category] = preferred_topic_order
    return assessment_framework
