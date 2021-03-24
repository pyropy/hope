from typing import List, Optional
from app.models.core import DBCoreModel
from pydantic import validator


# ###
# Presentation models
# ### 

class PresentationModelCore(DBCoreModel):
    name_ru: str
    description: str

class PresentationCreateModel(PresentationModelCore):
    fk: int
    key: str


class PresentationMediaCore(DBCoreModel):
    order: int
    url: str
    key: str

class PresentationMediaInDB(PresentationMediaCore):
    pass

class PresentationMediaCreate(PresentationMediaCore):
    fk: int

class PresentationInDB(PresentationModelCore):
    id: int
    images: List[PresentationMediaInDB]
    audio: List[PresentationMediaInDB]

# ###
# Book models
# ###

class BookModelCore(DBCoreModel):
    name_ru: str
    description: str

class BookPostModel(BookModelCore):
    fk: int
    key: str

class BookCreateModel(BookPostModel):
    url: str

class BookInDB(BookModelCore):
    id: int
    url: str
    key: str

# ###
# Video models
# ###

class VideoModelCore(DBCoreModel):
    name_ru: str
    description: str

class VideoPostModelYT(VideoModelCore):
    fk: int
    url: str

class VideoPostModelCDN(VideoModelCore):
    fk: int
    key: str

class VideoCreateModel(VideoModelCore):
    fk: int
    url: str
    key: Optional[str]

class VideoInDB(VideoModelCore):
    id: int
    url: str
    key: Optional[str]

# ###
# Game models
# ###

class GameModelCore(DBCoreModel):
    name_ru: str
    description: str
    url: str

class GamePostModel(GameModelCore):
    fk: int

class GameCreateModel(GamePostModel):
    pass

class GameInDB(GameModelCore):
    id: int

# ###
# Structure models
# ###

# grades
class GradeCoreModel(DBCoreModel):
    name_en: str
    name_ru: str
    background_key: str

class GradePostModel(GradeCoreModel):
    pass

class GradeCreateModel(GradeCoreModel):
    background: str

class GradeInDB(GradeCoreModel):
    id: int
    background: str

# grade response
class GradeResponse(DBCoreModel):
    grades: List[GradeInDB]

# subjects
class SubjectGetModel(DBCoreModel):
    grade_name_en: str

class SubjectCoreModel(DBCoreModel):
    fk: int
    name_en: str
    name_ru: str
    background_key: str

class SubejctPostModel(SubjectCoreModel):
    pass

class SubjectCreateModel(SubjectCoreModel):
    background: str

class SubjectInDB(SubjectCoreModel):
    id: int
    background: str

# subject response
class SubjectResponse(DBCoreModel):
    fk: int
    path: str
    subjects: List[SubjectInDB]

# branches
class BranchGetModel(DBCoreModel):
    grade_name_en: str
    subject_name_en: str

class BranchCoreModel(DBCoreModel):
    fk: int
    name_en: str
    name_ru: str
    background_key: str

class BranchPostModel(BranchCoreModel):
    pass

class BranchCreateModel(BranchCoreModel):
    background: str

class BranchInDB(BranchCoreModel):
    id: int
    background: str

# branch response
class BranchResponse(DBCoreModel):
    fk: int
    path: str
    branches: List[BranchInDB]

# lectures
class LectureGetModel(DBCoreModel):
    grade_name_en: str
    subject_name_en: str
    branch_name_en: str

class LectureCoreModel(DBCoreModel):
    fk: int
    name_en: str
    name_ru: str
    description: str
    background_key: str

class LecturePostModel(LectureCoreModel):
    pass

class LectureCreateModel(LectureCoreModel):
    background: str

class LectureInDB(LectureCoreModel):
    id: int
    background: str

# lecture response
class LectureResponse(DBCoreModel):
    fk: int
    path: str
    lectures: List[LectureInDB]

# material response
class MaterialResponseModel(DBCoreModel):
    fk: int
    video: VideoInDB
    game: GameInDB
    book: BookInDB
    practice: PresentationInDB
    theory: PresentationInDB
