from typing import List, Union
from app.db.repositories.base import BaseDBRepository
from app.db.repositories.private.queries import *
from asyncpg.exceptions import ForeignKeyViolationError

from fastapi import HTTPException

# import models
from app.models.private import PresentationCreateModel, PresentationInDB, PresentationMediaInDB, PresentationMediaCreate

import logging

logger = logging.getLogger(__name__)

class PrivateDBRepository(BaseDBRepository):

    async def insert_theory(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table='theory')

    async def insert_practice(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate]) -> PresentationInDB:
        return await self.__insert_presentation(presentation=presentation, images=images, audio=audio, table='practice')

    async def __insert_presentation(self, *, presentation: PresentationCreateModel, images: List[PresentationMediaCreate], audio: List[PresentationMediaCreate], table: Union['theory', 'practice']) -> PresentationInDB:
        
        query = insert_presentation_query(
            presentation=table, 
            fk=presentation.fk,
            name_ru=presentation.name_ru,
            description=presentation.description,
            key=presentation.key)

        images_query = insert_presentation_media_query(
            presentation=table,
            media_type='image',
            medium=images,
        )

        audio_query = insert_presentation_media_query(
            presentation=table,
            media_type='audio',
            medium=audio,
        )

        try:
            inserted_presentation = await self.db.fetch_one(query=query)
            inserted_images = await self.db.fetch_all(query=images_query)
            inserted_audio = await self.db.fetch_all(query=audio_query) 

            images = []
            audios = []
            for image in inserted_images:
                images.append(PresentationMediaInDB(**image))
            for audio in inserted_audio:
                audios.append(PresentationMediaInDB(**audio))

            return PresentationInDB(
                id=inserted_presentation['id'], 
                name_ru=inserted_presentation['name_ru'], 
                description=inserted_presentation['description'], 
                images=images,
                audio=audios)

        except ForeignKeyViolationError as e:
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT {table} ---")
            logger.error(e)
            logger.error(f"--- ForeignKeyViolationError RAISED TRYING TO INSERT {table} ---")
            raise HTTPException(status_code=404, detail=f"Insert {table} raised ForeignKeyViolationError. No such key in table lectures.")
        except Exception as e:
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {table} ---")
            logger.error(e)
            logger.error(f"--- ERROR RAISED TRYING TO INSERT {table} ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to insert {table}. Exited with {e}")
            