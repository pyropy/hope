from app.db.repositories.public.insert.insert import PublicDBInsertRepository
from app.db.repositories.public.select.select import PublicDBSelectRepository

class PublicDBRepository(
    PublicDBInsertRepository,
    PublicDBSelectRepository):
    pass