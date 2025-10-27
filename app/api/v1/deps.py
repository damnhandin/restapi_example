from fastapi import Request

from app.db.database import Database


async def get_db(request: Request) -> Database:
    return request.app.state.db
