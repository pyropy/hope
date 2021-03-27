def update_grades_query() -> str:
    pass

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