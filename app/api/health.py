from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("")
async def health():
    return {"status": "ok"}
