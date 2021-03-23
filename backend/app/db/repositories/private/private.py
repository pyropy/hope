from app.db.repositories.private.insert.insert import PrivateDBInsertRepository
from app.db.repositories.private.select.select import PrivateDBSelectRepository

class PrivateDBRepository(PrivateDBInsertRepository, PrivateDBSelectRepository):
    pass