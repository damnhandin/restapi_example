from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.schemas import AnswerRead


class QuestionBase(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswersRead(QuestionRead):
    answers: list["AnswerRead"] = Field(default_factory=list)


class QuestionsRead(BaseModel):
    questions: list[QuestionRead]
