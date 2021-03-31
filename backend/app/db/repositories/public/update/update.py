from fastapi import HTTPException

from app.db.repositories.public.update.queries import *

from app.db.repositories.base import BaseDBRepository

# update models
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

import logging

logger = logging.getLogger(__name__)

class PublicDBUpdateRepository(BaseDBRepository):

    async def update_video(self, *, updated: UpdateVideoModel) -> VideoInDB:
        response = await self.__update(query=update_video_query(name_ru=updated.name_ru, url=updated.url, description=updated.description))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table video")

        return VideoInDB(**response)

    async def update_game(self, *, updated: UpdateGameModel) -> GameInDB:
        response = await self.__update(query=update_game_query(name_ru=updated.name_ru, url=updated.url, description=updated.description))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table game")

        return GameInDB(**response)

    async def update_about_us(self, *, updated: UpdateAboutUsModel) -> AboutUsInDB:
        response = await self.__update(query=update_about_us_query(order_number=updated.order, title=updated.title, description=updated.description, svg=updated.svg))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table about us")

        return AboutUsInDB(**response)

    async def update_faq(self, *, updated: UpdateFAQModel) -> FAQInDB:
        response = await self.__update(query=update_faq_query(id=updated.id, question=updated.question, answer=updated.answer))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table FAQ")

        return FAQInDB(**response)


    async def update_instruction(self, *, updated: UpdateInstructionModel) -> InstructionInDB:
        response = await self.__update(query=update_instruction_query(order_number=updated.order, title=updated.title, description=updated.description))
        if not response:
            raise HTTPException(status_code=404, detail="Ooops! Didn't find anything to update in table Instruction")

        return InstructionInDB(**response)


    async def __update(self, query) -> None:
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR RAISED TRYING TO UPDATE PUBLIC ---")
            logger.error(e)
            logger.error("--- ERROR RAISED TRYING TO UPDATE PUBLIC ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to update public. Exited with {e}")

        return response
