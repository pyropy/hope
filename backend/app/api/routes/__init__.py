from fastapi import APIRouter

# private routes
from app.api.routes.private.post import router as private_post_router
from app.api.routes.private.put import router as private_put_router
from app.api.routes.private.get import router as private_get_router
from app.api.routes.private.delete import router as private_delete_router
# public routes
from app.api.routes.public.post import router as public_post_router
from app.api.routes.public.get import router as public_get_router
from app.api.routes.public.put import router as public_put_router
from app.api.routes.public.delete import router as public_delete_router

router = APIRouter()

# private routes
router.include_router(private_post_router, prefix='/private', tags=["private"])
router.include_router(private_put_router, prefix='/private', tags=["private"])
router.include_router(private_get_router, prefix='/private', tags=["private"])
router.include_router(private_delete_router, prefix="/private", tags=["private"])

# public routes
router.include_router(public_post_router, prefix='/public', tags=["public"])
router.include_router(public_get_router, prefix='/public', tags=["public"])
router.include_router(public_put_router, prefix='/public', tags=["public"])
router.include_router(public_delete_router, prefix='/public', tags=["public"])
