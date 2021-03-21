from typing import List
from app.models.core import DBCoreModel



class PresentationModelCore(DBCoreModel):
    name_ru: str
    description: str

class PresentationCreateModel(PresentationModelCore):
    fk: int
    key: str


class PresentationMediaCore(DBCoreModel):
    order: int
    url: str

class PresentationMediaInDB(PresentationMediaCore):
    pass

class PresentationMediaCreate(PresentationMediaCore):
    fk: int

class PresentationInDB(PresentationModelCore):
    id: int
    images: List[PresentationMediaInDB]
    audio: List[PresentationMediaInDB]
