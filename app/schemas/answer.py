from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnswerBase(BaseModel):
    user_id: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=10_000)


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
