from app.db.repositories.private.insert.insert import PrivateDBInsertRepository
from app.db.repositories.private.select.select import PrivateDBSelectRepository
from app.db.repositories.private.delete.delete import PrivateDBDeleteRepository

class PrivateDBRepository(PrivateDBInsertRepository, PrivateDBSelectRepository, PrivateDBDeleteRepository):
    pass