from typing import Tuple, List

from data_assessment_agent.model.db_model import DbSuggestedResponse
from data_assessment_agent.test.provider.question_provider import create_dummy_question


def create_suggestion_response():
    question = create_dummy_question()
    return DbSuggestedResponse(
        title="Yes", subtitle="Yes", body="Yes, confirmed", question=question
    )


def create_multiple_suggestions() -> Tuple[str, List[str]]:
    answer = "The data transformations in our system are really complex. We have very complicated mappings with lookups and also heavy usage of fuzzy matching."
    suggestions = [
        "The data transformations and computations are relatively straightforward, involving basic operations such as sorting, filtering, and simple arithmetic calculations. This level of complexity is suitable for tasks that require minimal data manipulation.",
        "The complexity of data transformations and computations is moderate, incorporating more advanced operations like data normalization, aggregation, and basic statistical analysis. This level is appropriate for projects that need a deeper understanding of the data without requiring highly complex algorithms.",
        "Data transformations and computations are highly complex, involving sophisticated algorithms for machine learning, predictive analytics, and data mining. This complexity level is necessary for tasks that demand a comprehensive analysis and insights from large and diverse datasets.",
    ]
    return answer, suggestions


def create_multiple_suggestions_2() -> Tuple[str, List[str]]:
    answer = "Increased profitability and work life balance for employees."
    suggestions = [
        "No, this is sensitive information that we cannot disclose at this moment.",
        "Partially, while improving customer satisfaction is a clear objective, I need to further understand the full scope of our business goals.",
        "Yes, the main goals include increasing profitability, expanding market share, and enhancing customer satisfaction to ensure long-term success.",
    ]
    return answer, suggestions
