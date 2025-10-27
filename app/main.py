import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.core.config import Config, load_config
from app.core.logging import setup_logging
from app.db.database import Database

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("🚀 Запускаем Q&A API...")
    # startup
    config: Config = load_config(path=".env")
    db = Database(db_config=config.db, echo=False)

    app.state.db = db
    try:
        yield
    finally:
        logger.info("🛑 Stopping Q&A API...")

    await app.state.db.engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="Q&A API", lifespan=lifespan)
    app.include_router(api_router, tags=["Q&A API"])
    return app


if __name__ == "__main__":
    uvicorn.run(
        "app.main:create_app", host="0.0.0.0", port=8080, factory=True
    )
