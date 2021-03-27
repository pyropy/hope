from fastapi import HTTPException

from app.db.repositories.private.update.queries import *

from app.db.repositories.base import BaseDBRepository

import logging

logger = logging.getLogger(__name__)

class PrivateDBUpdateRepository(BaseDBRepository):

    async def update_grade_links(self, *, grades) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table grade by keys
        """
        keys = list(grades.keys())
        links = list(grades.values())
        await self.__update(query=update_grade_links_query(keys=keys, links=links))

    async def update_subject_links(self, *, subjects) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table subject by keys
        """
        keys = list(subjects.keys())
        links = list(subjects.values())
        await self.__update(query=update_subject_links_query(keys=keys, links=links))

    async def update_branch_links(self, *, branches) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table branch by keys
        """
        keys = list(branches.keys())
        links = list(branches.values())
        await self.__update(query=update_branch_links_query(keys=keys, links=links))

    async def update_lecture_links(self, *, lectures) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table lecture by keys
        """
        keys = list(lectures.keys())
        links = list(lectures.values())
        await self.__update(query=update_lecture_links_query(keys=keys, links=links))


    async def update_book_links(self, *, book) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table book by keys
        """
        keys = list(book.keys())
        links = list(book.values())
        await self.__update(query=update_book_links_query(keys=keys, links=links))

    # presentation prats
    async def update_presentation_part_links(self, *, prats, presentation, media_type) -> None:
        """
        Accepts dict with keys = 'background_key' and value = 'sharing link'
        Updates table (theory | practice)_(image | audio) by keys
        """
        keys = list(prats.keys())
        links = list(prats.values())
        await self.__update(query=update_presentation_part_links_query(keys=keys, links=links, presentation=presentation, media_type=media_type))


    async def __update(self, *, query) -> None:
        try:
            updated = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR TRYING TO UPDATE ---")
            logger.error(e)
            logger.error("--- ERROR TRYING TO UPDATE ---")
            raise HTTPException(status_code=400, detail=f"Error raised trying to update table. Query: {query}. Exited with {e}")

        return updated