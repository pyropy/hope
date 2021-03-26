
def select_grades_query(ids=None) -> str:
    if ids:
        available = ','.join(map(str,ids))
        return \
            f"SELECT (private.select_grades_by_ids('{available}')).*"
    else:
        return \
            f"SELECT (private.select_all_grades()).*"

def select_subject_query(fk, ids=[]) -> str:
    if ids:
        available = ','.join(map(str,ids))
        return \
            f"SELECT (private.select_subjects_by_ids('{available}', {fk})).*"
    else:
        return \
            f"SELECT (private.select_all_subjects({fk})).*"

def select_branch_query(fk) -> str:
    return \
        f"SELECT (private.select_all_branches({fk})).*"

def select_lecture_query(fk) -> str:
    return \
        f"SELECT (private.select_all_lectures({fk})).*"

def get_grade_by_name_query(grade_name) -> str:
    return \
        f"SELECT (private.select_grade_by_name('{grade_name}')).*"

def get_subject_by_name_query(fk, subject_name) -> str:
    return \
        f"SELECT (private.select_subject_by_name('{subject_name}', {fk})).*"

def get_branch_by_name_query(fk, branch_name) -> str:
    return \
        f"SELECT (private.select_branch_by_name('{branch_name}', {fk})).*"

def get_lecture_by_name_query(fk, lecture_name) -> str:
    return \
        f"SELECT (private.select_lecture_by_name('{lecture_name}', {fk})).*"


# ###
# material queries
# ###
def select_material_query(fk) -> str:
    return \
        f"SELECT (private.select_material({fk})).*"

def select_one_material_query(fk, table) -> str:
    return \
        f"SELECT (private.select_{table}({fk})).*"


def select_material_parts(fk, presentation, media_type) -> str:
    return \
        f"SELECT (private.select_{presentation}_{media_type}({fk})).*"


