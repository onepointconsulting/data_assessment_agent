from pydantic import BaseModel, Field

class QuestionType(BaseModel):
    is_yes_no_question: bool = Field(..., description="Indicates whether you can answer this question using a yes or no response")


question_type_spec = {
    "name": "question_type",
    "description": "Question type, whether yes or no",
    "type": "object",
    "parameters": QuestionType.model_json_schema(),
}