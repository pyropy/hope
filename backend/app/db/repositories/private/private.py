from typing import List
from app.db.repositories.base import BaseDBRepository
from app.db.repositories.private.queries import *

# import models
from app.models.private import PresentationCreateModel, PresentationInDB, PresentationMediaInDB, PresentationMediaCreate

import logging

logger = logging.getLogger(__name__)

class PrivateDBRepository(BaseDBRepository):

    async def insert_theory(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:

        theory_query = insert_presentation_query(
            presentation='theory', 
            fk=presentation.fk,
            name_ru=presentation.name_ru,
            description=presentation.description,
            key=presentation.key)

        images_query = insert_presentation_media_query(
            presentation='theory',
            media_type='image',
            medium=images,
        )

        audio_query = insert_presentation_media_query(
            presentation='theory',
            media_type='audio',
            medium=audio,
        )

        try:
            inserted_theory = await self.db.fetch_one(query=theory_query)
            inserted_images = await self.db.fetch_all(query=images_query)
            inserted_audio = await self.db.fetch_all(query=audio_query) 

            images = []
            audios = []
            for image in inserted_images:
                images.append(PresentationMediaInDB(**image))
            for audio in inserted_audio:
                audios.append(PresentationMediaInDB(**audio))

            return PresentationInDB(
                id=inserted_theory['id'], 
                name_ru=inserted_theory['name_ru'], 
                description=inserted_theory['description'], 
                images=images,
                audio=audios)

        except Exception as e:
            logger.error("--- ERROR RAISED TRYING TO INSERT THEORY ---")
            logger.error(e)
            logger.error("--- ERROR RAISED TRYING TO INSERT THEORY ---")


        
