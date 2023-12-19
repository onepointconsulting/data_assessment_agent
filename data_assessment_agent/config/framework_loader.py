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
    assessment_framework = AssessmentFramework(categories={})
    for category, properties in framework_dict.items():
        questions = properties.get("questions", [])
        framework_questions = [
            Question(
                category=question["category"],
                question=question["question"],
                score=question["score"],
            )
            for question in questions
        ]
        assessment_framework.categories[category] = framework_questions
    return assessment_framework
