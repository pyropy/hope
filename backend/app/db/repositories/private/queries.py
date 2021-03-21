from typing import List

from app.models.private import PresentationMediaCreate

import logging

logger = logging.getLogger(__name__)


BANNED_KEY_WORDS = [
    'DELETE',
    'DROP',
    'UPDATE',
    'SET',
    'SELECT',
]

def filter(string) -> bool:
    for key in BANNED_KEY_WORDS:
        if key in string:
            return False
    return True

def warn_injection():
    logger.warn("--- CREATING QUERY ---")
    logger.error("Query filter did not pass. Potential SQL injection. Aborting!")
    logger.warn("--- CREATING QUERY ---")

def insert_grades_query(name_en, name_ru, background) -> str:

    if filter(f"{name_en} {name_ru} {background}"):
        return \
        f'INSERT INTO private.grade ' \
        f'(name_en, name_ru, background) ' \
        f'VALUES ({name_en}, {name_ru}, {background})'
    else:
        warn_injection()
        return None
        

def insert_video_query(fk, name_ru, description, key, url) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {url}"):
        return \
        f'INSERT INTO private.video '\
        f'(fk, url, name_ru, description, key)'
        f'VALUES ({fk}, {url}, {name_ru}, {description}, {key})'
        f'RETURNING fk, url, name_ru, description, key'
    else:
        warn_injection()
        return None

def insert_book_query(fk, name_ru, description, key, url) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {url}"):
        return \
        f'INSERT INTO private.book '\
        f'(fk, url, name_ru, description, key) '
        f'VALUES ({fk}, {url}, {name_ru}, {description}, {key}) '
        f'RETURNING fk, url, name_ru, description, key'
    else:
        warn_injection()
        return None

def insert_presentation_query(presentation, fk, name_ru, description, key) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {presentation}"):
        return \
        f'INSERT INTO private.{presentation} ' \
        f'(fk, name_ru, description, key) ' \
        f"VALUES ({fk}, '{name_ru}', '{description}', '{key}') " \
        f'RETURNING fk AS id, name_ru, description'
    else:
        warn_injection()
        return None

def insert_presentation_media_query(presentation, media_type , medium: List[PresentationMediaCreate]) -> str:

    if filter(f"{media_type} {presentation}"):
        query = \
        f'INSERT INTO private.{presentation}_{media_type} '\
        f'(fk, "order", url) ' \
        f'VALUES '
        for media in medium:
            if filter(f"{media.fk}, {media.order}, {media.url}"):
                query += f"({media.fk}, {media.order}, '{media.url}'), "
            else:
                warn_injection()
                return None

        query = query[:-2]
        query += ' RETURNING "order", url'
        return query
    else:
        warn_injection()
        return None




