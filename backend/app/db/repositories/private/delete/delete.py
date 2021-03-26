from fastapi import HTTPException

from app.db.repositories.base import BaseDBRepository

from app.db.repositories.private.delete.queries import *


from app.models.private import GradeInDB

import logging

logger = logging.getLogger(__name__)

class PrivateDBDeleteRepository(BaseDBRepository):

    async def delete_grade(self, *, id) -> int:
        return await self.__delete(query=delete_grade_query(id=id))

    async def delete_subject(self, *, id) -> int:
        return await self.__delete(query=delete_subject_query(id=id))

    async def delete_branch(self, *, id) -> int:
        return await self.__delete(query=delete_branch_query(id=id))

    async def delete_lecture(self, *, id) -> int:
        return await self.__delete(query=delete_lecture_query(id=id))

    async def delete_theory(self, *, id) -> int:
        return await self.__delete(query=delete_theory_query(id=id))

    async def delete_practice(self, *, id) -> int:
        return await self.__delete(query=delete_practice_query(id=id))

    async def delete_book(self, *, id) -> int:
        return await self.__delete(query=delete_book_query(id=id))

    async def delete_video(self, *, id) -> int:
        return await self.__delete(query=delete_video_query(id=id))

    async def delete_game(self, *, id) -> None:
        await self.db.fetch_one(query=delete_game_query(id=id))


    async def __delete(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
            key = response['key']
        except Exception as e:
            logger.error("--- ERROR TRYING TO DELETE ---")
            logger.error(e)
            logger.error("--- ERROR TRYING TO DELETE ---")
            raise HTTPException(status_code=400, detail=f"Unhandled error trying to delete. Exited with {e}. Query: {query}")

        if not key:
            raise HTTPException(status_code=404, detail="Trying to delete returned nothing.")
    
        return key