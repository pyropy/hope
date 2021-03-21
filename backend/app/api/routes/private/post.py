from fastapi import APIRouter
from fastapi import Depends, Body

from boto3 import Session

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.models.private import PresentationCreateModel, PresentationMediaCreate

from app.db.repositories.private.queries import insert_grades_query
router = APIRouter()

@router.post("/practice", )
async def create_private_practice(
    presentation: PresentationCreateModel = Body(...),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository))
    ) -> None:
    
    # get all keys for a given prefix
    keys = cdn_repo.get_object_keys(prefix=presentation.key)
    img_prefix = presentation.key + ('/img' if presentation.key[-1] != '/' else 'img')
    mp3_prefix = presentation.key + ('/mp3' if presentation.key[-1] != '/' else 'mp3')

    image_key_order = cdn_repo.get_key_order_pairs(prefix=img_prefix)
    audio_key_order = cdn_repo.get_key_order_pairs(prefix=mp3_prefix)

    image = cdn_repo.get_sharing_links_from_keys(prefix=img_prefix)
    audio = cdn_repo.get_sharing_links_from_keys(prefix=mp3_prefix)

    images = []
    for key, value in image.items():
        try:
            images.append(PresentationMediaCreate(order=image_key_order[key], url=value, fk=presentation.fk))
        except: 
            pass

    audios = []
    for key, value in audio.items():
        try:
            audios.append(PresentationMediaCreate(order=audio_key_order[key], url=value, fk=presentation.fk))
        except:
            pass

    response = await db_repo.insert_theory(presentation=presentation, images=images, audio=audios)

    return response
