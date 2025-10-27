import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.v1.deps import get_db
from app.schemas import AnswerRead
from app.schemas.answer import AnswerCreate

if TYPE_CHECKING:
    from app.db.database import Database

logger = logging.getLogger(__name__)
router = APIRouter(tags=["answers"])


@router.post(
    "/questions/{question_id}/answers",
    response_model=AnswerRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer_endpoint(
    question_id: int,
    payload: AnswerCreate,
    db: "Database" = Depends(get_db),
):
    try:
        return await db.create_answer_for_question(
            question_id=question_id, data=payload
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        ) from None
    except Exception as e:
        logger.exception(f"Unexpected error {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.get("/answers/{answer_id}", response_model=AnswerRead)
async def get_answer_endpoint(
    answer_id: int,
    db: "Database" = Depends(get_db),
):
    try:
        answer = await db.get_answer_by_id(answer_id=answer_id)
    except Exception as e:
        logger.exception(f"Unexpected error {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        ) from None
    return answer


@router.delete(
    "/answers/{answer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_answer_endpoint(
    answer_id: int,
    db: "Database" = Depends(get_db),
):
    try:
        deleted = await db.delete_answer_by_id(answer_id=answer_id)
    except Exception as e:
        logger.exception(f"Unexpected error {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        ) from None
    return None
