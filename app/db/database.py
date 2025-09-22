import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from app.core.config import DbConfig
from app.db.models import AnswerOrm, Base, QuestionOrm

if TYPE_CHECKING:
    from app.schemas.answer import AnswerCreate
    from app.schemas.question import QuestionCreate

logger = logging.getLogger(__name__)


class Database:
    def __init__(
        self,
        db_config: DbConfig | None,
        echo=True,
        pool_size=5,
        max_overflow=10,
    ):
        self.db_config = db_config
        self.engine = create_async_engine(
            url=self.db_config.database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_maker: async_sessionmaker = async_sessionmaker(self.engine)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # ---------- ANSWERS ----------

    async def create_answer_for_question(
        self, question_id: int, data: "AnswerCreate"
    ) -> AnswerOrm:
        async with self.session_maker() as session:  # type: AsyncSession
            async with session.begin():
                answer = AnswerOrm(question_id=question_id, **data.model_dump())
                session.add(answer)
            await session.refresh(answer)
            return answer

    async def get_answer_by_id(self, answer_id: int) -> AnswerOrm | None:
        async with self.session_maker() as session:  # type: AsyncSession
            # тянем и связанный question, чтобы сразу можно было отдать наружу
            stmt = (
                select(AnswerOrm)
                .options(selectinload(AnswerOrm.question))
                .where(AnswerOrm.id == answer_id)
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def delete_answer_by_id(self, answer_id: int) -> bool:
        async with self.session_maker() as session:  # type: AsyncSession
            async with session.begin():
                # можно через delete() + returning, чтобы понять, было ли удаление
                stmt = delete(AnswerOrm).where(AnswerOrm.id == answer_id)
                result = await session.execute(stmt)
                # result.rowcount поддерживается в SA 2.0 для DML
                deleted = result.rowcount or 0
            return deleted > 0

    # ---------- QUESTIONS ----------

    async def list_questions(self) -> list[QuestionOrm]:
        async with self.session_maker() as session:  # type: AsyncSession
            stmt = (
                select(QuestionOrm)
                .options(selectinload(QuestionOrm.answers))
                .order_by(QuestionOrm.created_at.desc(), QuestionOrm.id.desc())
            )
            res = await session.execute(stmt)
            return list(res.scalars().all())

    async def create_question(self, data: "QuestionCreate") -> QuestionOrm:
        async with self.session_maker() as session:  # type: AsyncSession
            async with session.begin():
                question = QuestionOrm(**data.model_dump())
                session.add(question)
            # подтягиваем id/created_at
            await session.refresh(question)
            return question

    async def get_question(self, question_id: int) -> QuestionOrm | None:
        async with self.session_maker() as session:  # type: AsyncSession
            # session.get быстрее и короче, но без опций — поэтому комбинируем:
            stmt = (
                select(QuestionOrm)
                .options(selectinload(QuestionOrm.answers))
                .where(QuestionOrm.id == question_id)
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def delete_question_by_id(self, question_id: int) -> bool:
        async with self.session_maker() as session:  # type: AsyncSession
            async with session.begin():
                stmt = delete(QuestionOrm).where(QuestionOrm.id == question_id)
                result = await session.execute(stmt)
                deleted = result.rowcount or 0
            return deleted > 0
