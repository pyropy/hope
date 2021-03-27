from fastapi import APIRouter, Depends


from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository
from app.api.dependencies.updating import update_sharing_links_function

router = APIRouter()


# force update all links
@router.put("/update")
async def update_sharing_links(
    update_function = Depends(update_sharing_links_function)
    ) -> None:

    return None
  