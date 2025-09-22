from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import DbConfig


class Base(DeclarativeBase):
    pass


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
