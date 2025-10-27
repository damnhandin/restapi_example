import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import get_db
from app.db.database import Database
from app.schemas.question import (
    QuestionCreate,
    QuestionRead,
    QuestionsRead,
    QuestionWithAnswersRead,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("", response_model=QuestionsRead, status_code=status.HTTP_200_OK)
async def get_questions_endpoint(db: Database = Depends(get_db)):
    try:
        return {"questions": await db.list_questions()}
    except Exception:
        logger.exception("Database error", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.post("", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question_endpoint(
    payload: QuestionCreate,
    db: Database = Depends(get_db),
):
    try:
        return await db.create_question(data=payload)
    except Exception as e:
        logger.exception(f"Unexpected error {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.get(
    "/{question_id}",
    response_model=QuestionWithAnswersRead,
    status_code=status.HTTP_200_OK,
)
async def get_question_with_answers_endpoint(
    question_id: int, db: Database = Depends(get_db)
):
    try:
        question = await db.get_question(question_id=question_id)
    except Exception as e:
        logger.exception(f"Unexpected error {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question_endpoint(question_id: int, db: Database = Depends(get_db)):
    try:
        deleted = await db.delete_question_by_id(question_id=question_id)
    except Exception as e:
        logger.exception(f"Unexpected error {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None
    if not deleted:
        # Ничего не удалено — вопрос не найден
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        ) from None
    return None
