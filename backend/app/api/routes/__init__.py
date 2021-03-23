from fastapi import APIRouter

from app.api.routes.private.post import router as private_post_router
from app.api.routes.private.put import router as private_put_router
from app.api.routes.private.get import router as private_get_router

router = APIRouter()

# private routes
router.include_router(private_post_router, prefix='/private', tags=["private"])
router.include_router(private_put_router, prefix='/private', tags=["private"])
router.include_router(private_get_router, prefix='/private', tags=["private"])

# public routes
