from fastapi import APIRouter
from fastapi import Depends, Body
from starlette.status import HTTP_200_OK

from app.db.repositories.public.public import PublicDBRepository

from app.api.dependencies.database import get_db_repository

from app.db.repositories.parsers import parse_youtube_link

# request models
from app.models.public import UpdateVideoModel
from app.models.public import UpdateGameModel
from app.models.public import UpdateAboutUsModel
from app.models.public import UpdateFAQModel
from app.models.public import UpdateInstructionModel

# response models
from app.models.public import VideoInDB
from app.models.public import GameInDB
from app.models.public import AboutUsInDB
from app.models.public import FAQInDB
from app.models.public import InstructionInDB


router = APIRouter()


@router.put("/video/youtube", response_model=VideoInDB, name="public:update-video-youtube", status_code=HTTP_200_OK)
async def update_video(
    video: UpdateVideoModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> VideoInDB:
    if video.url:
        video.url = parse_youtube_link(link=video.url)
    response = await db_repo.update_video(updated=video)

    return response

@router.put("/game", response_model=GameInDB, name="public:update-game", status_code=HTTP_200_OK)
async def update_game(
    game: UpdateGameModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> GameInDB:
    response = await db_repo.update_game(updated=game)

    return response

@router.put("/about_us", response_model=AboutUsInDB, name="public:update-about_us", status_code=HTTP_200_OK)
async def update_about_us(
    about_us: UpdateAboutUsModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> AboutUsInDB:
    response = await db_repo.update_about_us(updated=about_us)

    return response

@router.put("/faq", response_model=FAQInDB, name="public:update-faq", status_code=HTTP_200_OK)
async def update_faq(
    faq: UpdateFAQModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> FAQInDB:
    response = await db_repo.update_faq(updated=faq)

    return response

@router.put("/instructions", response_model=InstructionInDB, name="public:update-instruction", status_code=HTTP_200_OK)
async def update_instruction(
    instruction: UpdateInstructionModel = Body(...),
    db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    ) -> InstructionInDB:
    response = await db_repo.update_instruction(updated=instruction)

    return response