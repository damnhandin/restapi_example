from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.schemas.answer import AnswerRead


class QuestionBase(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: int
    created_at: datetime
    answers: list["AnswerRead"] | None = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class QuestionsRead(BaseModel):
    questions: list[QuestionRead]
