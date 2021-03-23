from typing import List

from app.db.repositories.filter import filter, warn_injection
from app.models.private import PresentationMediaCreate

import logging

logger = logging.getLogger(__name__)



# ###
# Structure queries
# ###

def insert_grades_query(name_en, name_ru, background_key, background) -> str:

    if filter(f"{name_en} {name_ru} {background_key} {background}"):
        return \
        f'INSERT INTO private.grade ' \
        f'(name_en, name_ru, background_key, background) ' \
        f"VALUES ('{name_en}', '{name_ru}', '{background_key}', '{background}') " \
        f"RETURNING id, name_en, name_ru, background_key, background"
    else:
        warn_injection()
        return None
        

def insert_subject_query(fk, name_en, name_ru, background_key, background) -> str:

    if filter(f"{fk} {name_en} {name_ru} {background_key} {background}"):
        return \
        f"INSERT INTO private.subject "\
        f"(fk, name_en, name_ru, background_key, background) "\
        f"VALUES ({fk}, '{name_en}', '{name_ru}', '{background_key}', '{background}') " \
        f"RETURNING id, fk, name_en, name_ru, background_key, background"
    else:
        warn_injection()
        return None

def insert_branch_query(fk, name_en, name_ru, background_key, background) -> str:

    if filter(f"{fk} {name_en} {name_ru} {background_key} {background}"):
        return \
        f"INSERT INTO private.branch "\
        f"(fk, name_en, name_ru, background_key, background) "\
        f"VALUES ({fk}, '{name_en}', '{name_ru}', '{background_key}', '{background}') " \
        f"RETURNING id, fk, name_en, name_ru, background_key, background"
    else:
        warn_injection()
        return None

def insert_lecture_query(fk, name_en, name_ru, description, background_key, background) -> str:

    if filter(f"{fk} {name_en} {name_ru} {description} {background_key} {background}"):
        return \
        f"INSERT INTO private.lecture "\
        f"(fk, name_en, name_ru, description, background_key, background) "\
        f"VALUES ({fk}, '{name_en}', '{name_ru}', '{description}', '{background_key}', '{background}') " \
        f"RETURNING id, fk, name_en, name_ru, description, background_key, background"
    else:
        warn_injection()
        return None

# ###
# Material queries
# ###

def insert_video_query(fk, name_ru, description, key, url) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {url}"):
        return \
        f'INSERT INTO private.video ' \
        f'(fk, url, name_ru, description, key)' \
        f"VALUES ({fk}, '{url}', '{name_ru}', '{description}', '{key}')" \
        f'RETURNING fk AS id, url, name_ru, description, key'
    else:
        warn_injection()
        return None

def insert_book_query(fk, name_ru, description, key, url) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {url}"):
        return \
        f'INSERT INTO private.book ' \
        f'(fk, url, name_ru, description, key) ' \
        f"VALUES ({fk}, '{url}', '{name_ru}', '{description}', '{key}') " \
        f'RETURNING fk AS id, url, name_ru, description, key'
    else:
        warn_injection()
        return None

def insert_presentation_query(presentation, fk, name_ru, description, key) -> str:
    '''
    presentation: theory | practice
    fk: lecture id (id of lecture we are adding material to)
    name_ru: presentation name
    description: presentation description
    key: presentation key in cdn
    '''

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
    '''
    presentation: theory | practice
    media_type: image | audio
    medium: List of PresentationMediaCreate -> fk, url, order
        fk: id of lecture we are adding to
        url: sharing link
        order: order number in which it should be displayed when forming presentation
    '''


    if filter(f"{media_type} {presentation}"):
        query = \
        f'INSERT INTO private.{presentation}_{media_type} '\
        f'(fk, "order", url, key) ' \
        f'VALUES '
        for media in medium:
            if filter(f"{media.fk}, {media.order}, {media.url} {media.key}"):
                query += f"({media.fk}, {media.order}, '{media.url}', '{media.key}'), "
            else:
                warn_injection()
                return None

        query = query[:-2]
        query += ' RETURNING "order", url, key'
        return query
    else:
        warn_injection()
        return None

def insert_game_query(fk, name_ru, description, url) -> str:
    if filter(f"{fk} {name_ru} {description} {url}"):
        return \
        f"INSERT INTO private.game "\
        f"(fk, name_ru, description, url) "\
        f"VALUES ({fk}, '{name_ru}', '{description}', '{url}')"
    else:
        warn_injection()
        return None

# timestamp
def check_timestamp_is_set_query() -> str:
    return "SELECT COUNT(*) AS count FROM private.timestamp;"

def set_timestamp_to_now_query() -> str:
    return "INSERT INTO private.timestamp(last_update, is_updating)  VALUES(now(), 'f');"