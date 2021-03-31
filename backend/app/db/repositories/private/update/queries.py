from app.db.repositories.parsers import string_or_null

# Update links (auto update)

def update_grade_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT private.update_grade_links('{{{keys}}}', '{{{links}}}')"

def update_subject_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT private.update_subject_links('{{{keys}}}', '{{{links}}}')"

def update_branch_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT private.update_branch_links('{{{keys}}}', '{{{links}}}')"

def update_lecture_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT private.update_lecture_links('{{{keys}}}', '{{{links}}}')"


def update_book_links_query(keys, links) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT private.update_book_links('{{{keys}}}', '{{{links}}}')"


def update_presentation_part_links_query(keys, links, presentation, media_type) -> str:
    keys = list_to_string(keys)
    links = list_to_string(links)
    return \
        f"SELECT private.update_{presentation}_{media_type}_links('{{{keys}}}', '{{{links}}}')"

def list_to_string(list_) -> str:
    list_ = str(list_).replace('[','')
    list_ = str(list_).replace(']','')
    list_ = str(list_).replace("'",'')
    return list_


# Update data
def update_grade_query(id, name_ru, background_url, background_key) -> str:
    return \
        f"SELECT (private.update_grade({id}{string_or_null(name_ru, background_url, background_key)})).*"

def update_subject_query(id, name_ru, background_url, background_key) -> str:
    return \
        f"SELECT (private.update_subject({id}{string_or_null(name_ru, background_url, background_key)})).*"

def update_branch_query(id, name_ru,  background_url, background_key) -> str:
    return \
        f"SELECT (private.update_branch({id}{string_or_null(name_ru, background_url, background_key)})).*"

def update_lecture_query(id, name_ru, description, background_url, background_key) -> str:
    return \
        f"SELECT (private.update_lecture({id}{string_or_null(name_ru, description, background_url, background_key)})).*"

def update_video_query(id, name_ru, description, url) -> str:
    return \
        f"SELECT (private.update_video({id}{string_or_null(name_ru, description, url)})).*"

def update_game_query(id, name_ru, description, url) -> str:
    return \
        f"SELECT (private.update_game({id}{string_or_null(name_ru, description, url)})).*"
