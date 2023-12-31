from enum import StrEnum

from pydantic import BaseModel, Field


class Sentiment(StrEnum):
    VERY_NEGATIVE = "very negative"
    NEGATIVE = "negative"
    AMBIGUOUS = "ambiguous"
    POSITIVE = "positive"
    VERY_POSITIVE = "very positive"
    UNKNOWN = "unknown"


class AnswerSentiment(BaseModel):
    sentiment: Sentiment = Field(
        ..., description="The sentiment of the response related to its question"
    )


answer_sentiment_spec = {
    "name": "answer_sentiment",
    "description": "Gives the sentiment of an answer in relation to a question",
    "type": "object",
    "parameters": AnswerSentiment.model_json_schema(),
}
