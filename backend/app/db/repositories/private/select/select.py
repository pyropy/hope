from typing import List
from app.db.repositories.base import BaseDBRepository
from fastapi import HTTPException

# queries
from app.db.repositories.private.select.queries import *

# response models
from app.models.private import GradeInDB
from app.models.private import SubjectInDB
from app.models.private import BranchInDB
from app.models.private import LectureInDB

import logging

logger = logging.getLogger(__name__)

class PrivateDBSelectRepository(BaseDBRepository):

    async def get_grade_by_name(self, *, grade_name) -> GradeInDB:
        
        response = await self.__select_one(query=get_grade_by_name_query(grade_name=grade_name))

        return GradeInDB(**response)

    async def get_subject_by_name(self, *, grade_name, subject_name) -> SubjectInDB:
        # get grade id (fk for subject)
        grade = await self.get_grade_by_name(grade_name=grade_name)

        response = await self.__select_one(query=get_subject_by_name_query(fk=grade.id, subject_name=subject_name))
        return SubjectInDB(**response)

    async def get_branch_by_name(self, *, grade_name, subject_name, branch_name) -> BranchInDB:
        # get subject id (fk for branch)
        subject = await self.get_subject_by_name(grade_name=grade_name, subject_name=subject_name)

        response = await self.__select_one(query=get_branch_by_name_query(fk=subject.id, branch_name=branch_name))
        return BranchInDB(**response)

    async def get_lecture_by_name(self, *, grade_name, subject_name, branch_name, lecture_name) -> LectureInDB:
        # get branch id (fk for lecture)
        branch = await self.get_branch_by_name(grade_name=grade_name, subject_name=subject_name, branch_name=branch_name)

        response = await self.__select_one(query=get_lecture_by_name_query(fk=branch.id, lecture_name=lecture_name))
        return LectureInDB(**response)

    async def select_grades(self, *, ids=None) -> List[GradeInDB]:
        """
        Returns list of grades available to customer, or all of them in ids=None
        ids - list of grade ids available to customer
        """
        response_data = await self.__select_many(query=select_grades_query(ids=ids))

        response = []
        for data in response_data:
            response.append(GradeInDB(**data))

        return response        

    async def select_subjects(self, *, fk, ids=None) -> List[SubjectInDB]:
        """
        Returns list of subjects available to customer, or all of them in ids=None
        ids - list of subject ids available to customer
        """
        response_data = await self.__select_many(query=select_subject_query(fk=fk, ids=ids))

        response = []
        for data in response_data:
            response.append(SubjectInDB(**data))

        return response

    async def select_branches(self, *, fk) -> List[BranchInDB]:

        response_data = await self.__select_many(query=select_branch_query(fk=fk))

        response = []
        for data in response_data:
            response.append(BranchInDB(**data))

        return response

    async def select_lectures(self, *, fk) -> List[LectureInDB]:

        response_data = await self.__select_many(query=select_lecture_query(fk=fk))

        response = []
        for data in response_data:
            response.append(LectureInDB(**data))

        return response


    async def __select_many(self, *, query):
        try:
            response = await self.db.fetch_all(query=query)
        except Exception as e:
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            logger.error(e)
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to execute select query {query}. Error {e}")

        if not response:
            # remove query from fstring before deployment
            raise HTTPException(status_code=404, detail=f"Query found nothing! {query}")

        return response

    async def __select_one(self, *, query):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            logger.error(e)
            logger.error("--- SELECT QUERY RAISED UNHANDLED ERROR ---") 
            raise HTTPException(status_code=400, detail=f"Unhandled error raised trying to execute select query {query}. Error {e}")
        
        if not response:
            # remove query from fstring before deployment
            raise HTTPException(status_code=404, detail=f"Query found nothing! {query}")

        return response
