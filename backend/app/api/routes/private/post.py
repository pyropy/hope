from fastapi import APIRouter

router = APIRouter()

@router.post("/practice")
async def create_private_practice() -> None:
    pass