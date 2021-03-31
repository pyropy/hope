from fastapi import APIRouter
from fastapi import Depends
from starlette.status import HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository
from app.cdn.repositories.public.public import PublicYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository


router = APIRouter()

@router.delete("/theory", name="public:delete-theory", status_code=HTTP_200_OK)
async def delete_theory(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository))
    ):
    response = await db_repo.delete_theory()

    if response:
        cdn_repo.delete_folder(prefix=response)
        return {"Status": f"Successfully deleted {response} folder"}

    return {"Status": "Failed deleting. Database doesn't containt any entries for theory"}

@router.delete("/practice", name="public:delete-practice", status_code=HTTP_200_OK)
async def delete_practice(    
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository))
    ):
    response = await db_repo.delete_practice()

    if response:
        cdn_repo.delete_folder(prefix=response)
        return {"Status": f"Successfully deleted {response} folder"}

    return {"Status": "Failed deleting. Database doesn't containt any entries for practice"}

@router.delete("/book", name="public:delete-book", status_code=HTTP_200_OK)
async def delete_book(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    cdn_repo: PublicYandexCDNRepository = Depends(get_cdn_repository(PublicYandexCDNRepository))
    ):
    response = await db_repo.delete_book()

    if response:
        cdn_repo.delete_folder_by_inner_key(key=response)
        return {"Status": f"Successfully deleted {response} and parent folder"}

    return {"Status": "Failed deleting. Database doesn't containt any entries for book"}


@router.delete("/video/youtube", name="public:delete-video-youtube", status_code=HTTP_200_OK)
async def delete_video(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ):
    await db_repo.delete_video()
    return {"Status": "All gucci"}


@router.delete("/game", name="public:delete-game", status_code=HTTP_200_OK)
async def delete_game(
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ):
    await db_repo.delete_game()
    return {"Status": "All gucci"}

@router.delete("/about_us", name="public:delete-about_us", status_code=HTTP_200_OK)
async def delete_about_us(
    order_number: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ):
    await db_repo.delete_about_us(order_number=order_number)
    return {"Status": "All gucci"}

@router.delete("/faq", name="public:delete-faq", status_code=HTTP_200_OK)
async def delete_faq(
    id: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ):
    await db_repo.delete_faq(id=id)
    return {"Status": "All gucci"}

@router.delete("/instructions", name="public:delete-instructions", status_code=HTTP_200_OK)
async def delete_instruction(
    order_number: int,
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ):
    await db_repo.delete_instruction(order_number=order_number)
    return {"Status": "All gucci"}
