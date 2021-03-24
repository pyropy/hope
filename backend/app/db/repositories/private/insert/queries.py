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
        f"SELECT (insert_grade('{name_en}', '{name_ru}', '{background_key}', '{background}')).*"
    else:
        warn_injection()
        return None
        

def insert_subject_query(fk, name_en, name_ru, background_key, background) -> str:

    if filter(f"{fk} {name_en} {name_ru} {background_key} {background}"):
        return \
        f"SELECT (insert_subject({fk}, '{name_en}', '{name_ru}', '{background_key}', '{background}')).*"
    else:
        warn_injection()
        return None

def insert_branch_query(fk, name_en, name_ru, background_key, background) -> str:

    if filter(f"{fk} {name_en} {name_ru} {background_key} {background}"):
        return \
        f"SELECT (insert_branch({fk}, '{name_en}', '{name_ru}', '{background_key}', '{background}')).*"
    else:
        warn_injection()
        return None

def insert_lecture_query(fk, name_en, name_ru, description, background_key, background) -> str:

    if filter(f"{fk} {name_en} {name_ru} {description} {background_key} {background}"):
        return \
        f"SELECT (insert_lecture({fk}, '{name_en}', '{name_ru}', '{description}', '{background_key}', '{background}')).*"
    else:
        warn_injection()
        return None

# ###
# Material queries
# ###

def insert_video_query(fk, name_ru, description, key, url) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {url}"):
        return \
        f"SELECT (insert_video({fk}, '{name_ru}', '{description}', '{key}', '{url}')).*"
    else:
        warn_injection()
        return None

def insert_game_query(fk, name_ru, description, url) -> str:
    if filter(f"{fk} {name_ru} {description} {url}"):
        return \
        f"SELECT (insert_game({fk}, '{name_ru}', '{description}', '{url}')).*"
            
    else:
        warn_injection()
        return None

def insert_book_query(fk, name_ru, description, key, url) -> str:

    if filter(f"{fk} {name_ru} {description} {key} {url}"):
        return \
        f"SELECT (insert_book({fk}, '{name_ru}', '{description}', '{key}', '{url}')).*"

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

    if presentation == "theory": 
        return \
            f"SELECT (insert_theory({fk}, '{name_ru}', '{description}', '{key}')).*"
    else:
        pass

def insert_presentation_media_query(presentation, media_type , medium: List[PresentationMediaCreate]) -> str:
    '''
    presentation: theory | practice
    media_type: image | audio
    medium: List of PresentationMediaCreate -> fk, url, order
        fk: id of lecture we are adding to
        url: sharing link
        order: order number in which it should be displayed when forming presentation
    '''
    foreign_keys = []
    order_numbers = []
    urls = []
    keys = []
    for media in medium:
        foreign_keys.append(media.fk)
        order_numbers.append(media.order)
        urls.append(media.url)
        keys.append(media.key)

    foreign_keys = ','.join(map(str,foreign_keys))
    order_numbers = ','.join(map(str,order_numbers))
    urls = ','.join(map(str,urls))
    keys = ','.join(map(str,keys))

    if media_type == "image":
        return \
            f"SELECT (insert_theory_image('{foreign_keys}', '{order_numbers}', '{{{urls}}}', '{{{keys}}}')).*"
    elif media_type == "audio":
        return \
            f"SELECT (insert_theory_audio('{foreign_keys}', '{order_numbers}', '{{{urls}}}', '{{{keys}}}')).*"


# timestamp
def check_timestamp_is_set_query() -> str:
    return "SELECT COUNT(*) AS count FROM private.timestamp;"

def set_timestamp_to_now_query() -> str:
    return "INSERT INTO private.timestamp(last_update, is_updating)  VALUES(now(), 'f');"