from fastapi import APIRouter

from app.api.routes.private.post import router as private_post_router

router = APIRouter()

router.include_router(private_post_router, prefix='/private', tags=["private"])
