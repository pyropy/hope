from fastapi import Depends

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

async def update_sharing_links_function(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    ) -> None:

    grades = await db_repo.select_all_grades()
    subjects = await db_repo.select_all_subjects()
    branches = await db_repo.select_all_branches()
    lectures = await db_repo.select_all_lectures()
    
    books = await db_repo.select_all_books()

    theory_images = await db_repo.select_all_presentation_parts(presentation='theory', media_type='image')
    theory_audio = await db_repo.select_all_presentation_parts(presentation='theory', media_type='audio')

    practice_images = await db_repo.select_all_presentation_parts(presentation='practice', media_type='image')
    practice_audio = await db_repo.select_all_presentation_parts(presentation='practice', media_type='audio')

    keys = cdn_repo.create_key_list_from_lists_of_objects(
        grades=grades,
        subjects=subjects,
        branches=branches,
        lectures=lectures,
        books=books,
        theory_images=theory_images,
        theory_audio=theory_audio,
        practice_images=practice_images,
        practice_audio=practice_audio,)

    if grades:
        updated_grades = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['grades'])
        await db_repo.update_grade_links(grades=updated_grades)

    if subjects:
        updated_subjects = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['subjects'])
        await db_repo.update_subject_links(subjects=updated_subjects)

    if branches:
        updated_branches = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['branches'])
        await db_repo.update_branch_links(branches=updated_branches)
    
    if lectures:
        updated_lectures = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['lectures'])
        await db_repo.update_lecture_links(lectures=updated_lectures)

    if books:
        updated_books = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['books'])
        await db_repo.update_book_links(book=updated_books)

    if theory_images:
        updated_theory_images = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['theory_images'])
        await db_repo.update_presentation_part_links(prats=updated_theory_images, presentation='theory', media_type='image')
    if theory_audio:
        updated_theory_audio = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['theory_audio'])
        await db_repo.update_presentation_part_links(prats=updated_theory_audio, presentation='theory', media_type='audio')

    if practice_images:
        updated_practice_images = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['practice_images'])
        await db_repo.update_presentation_part_links(prats=updated_practice_images, presentation='practice', media_type='image')
    if practice_audio:
        updated_practice_audio = cdn_repo.get_sharing_links_from_keys(list_of_objects=keys['practice_audio'])
        await db_repo.update_presentation_part_links(prats=updated_practice_audio, presentation='practice', media_type='audio')
