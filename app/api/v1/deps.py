from typing import Annotated

from fastapi import Query, Request

from app.db.database import Database

# Параметры пагинации по умолчанию
LimitDep = Annotated[int, Query(ge=1, le=100, description="Размер страницы (1..100)")]
OffsetDep = Annotated[int, Query(ge=0, description="Смещение")]


async def get_db(request: Request) -> Database:
    return request.app.state.db
