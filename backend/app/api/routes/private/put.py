from fastapi import APIRouter, Depends


from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

router = APIRouter()

@router.put("/sync")
async def sync_cdn_and_db(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    ) -> None:
    grades = await db_repo.select_all_grades()
    subjects = await db_repo.select_all_subjects()
    branches = await db_repo.select_all_branches()
    lectures = await db_repo.select_all_lectures()
    
    theory = await db_repo.select_all_presentation(presentation='theory')
    practice = await db_repo.select_all_presentation(presentation='practice')

    theory_images = await db_repo.select_all_presentation_parts(presentation='theory', media_type='image')
    theory_audio = await db_repo.select_all_presentation_parts(presentation='theory', media_type='audio')

    practice_images = await db_repo.select_all_presentation_parts(presentation='practice', media_type='image')
    practice_audio = await db_repo.select_all_presentation_parts(presentation='practice', media_type='audio')

    keys = cdn_repo.create_key_list_from_lists_of_objects(
        grades=grades,
        subjects=subjects,
        branches=branches,
        lectures=lectures,
        theory=theory,
        practice=practice,
        theory_images=theory_images,
        theory_audio=theory_audio,
        practice_images=practice_images,
        practice_audio=practice_audio,)

    prefix='subscription/'
    all_keys = cdn_repo.get_object_keys(prefix=prefix, update=True)
    
    # valid - keys present in both db and cdn (to be updated)
    # db_extra - keys present in db but not in cdn (to be deleted)
    # cdn_extra - keys present in cdn but not in db (to be inserted if "folder" or deleted if background) 
    (valid, db_extra, cdn_extra) = cdn_repo.compare(db_list_of_keys=keys, cdn_list_of_keys=all_keys)

    print("--- DB EXTRA ---")
    print(db_extra)
    print("--- DB EXTRA ---")

    print("--- CDN EXTRA ---")
    print(cdn_extra)
    print("--- CDN EXTRA ---")

    print("--- VALID ---")
    print(valid)
    print("--- VALID ---")

    # next - update sharing links from valid

    # then - split db_extra, valid in categories based on number of / in it
    # e.g. subscription/7-9/background.jpg = grade_extra
    # subscription/7-9/mathematics/background.jpg = subject_extra
    # etc...

    # after that - send valid lists to corresponding update function
    # send db_extra to corresponding delete functions

    # think what to do with cdn_extra

    return None