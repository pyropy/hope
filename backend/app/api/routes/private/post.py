from fastapi import APIRouter
from fastapi import Depends, Body
from starlette import status

from boto3 import Session

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

# Request models
from app.models.private import PresentationCreateModel, PresentationMediaCreate

# Response models
from app.models.private import PresentationInDB


from app.db.repositories.private.queries import insert_grades_query
router = APIRouter()

@router.post("/practice", response_model=PresentationInDB, name="private:post-practice", status_code=status.HTTP_201_CREATED)
async def create_private_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository))
    ) -> PresentationInDB:

    # get images and audio formed data    
    (images, audio) = cdn_repo.form_presentation_insert_data(prefix=presentation.key, fk=presentation.fk)
    # insert into database
    response = await db_repo.insert_practice(presentation=presentation, images=images, audio=audio)

    return response

@router.post("/theory", response_model=PresentationInDB, name="private:post-theory", status_code=status.HTTP_201_CREATED)
async def create_private_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository))
    ) -> PresentationInDB:

    # get images and audio formed data    
    (images, audio) = cdn_repo.form_presentation_insert_data(prefix=presentation.key, fk=presentation.fk)
    # insert into database
    response = await db_repo.insert_theory(presentation=presentation, images=images, audio=audio)

    return response
