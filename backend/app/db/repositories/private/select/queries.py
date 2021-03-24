from app.db.repositories.filter import filter, warn_injection

def select_grades_query(ids=None) -> str:
    if ids:
        available = ','.join(map(str,ids))
        return \
            f"SELECT (select_grades_by_ids('{available}')).*"
    else:
        return \
            f"SELECT (select_all_grades()).*"

def select_subject_query(fk, ids=[]) -> str:
    if ids:
        available = ','.join(map(str,ids))
        return \
            f"SELECT (select_subjects_by_ids('{available}', {fk})).*"
    else:
        return \
            f"SELECT (select_all_subjects({fk})).*"

def select_branch_query(fk) -> str:
    return \
        f"SELECT * FROM private.branch WHERE fk = {fk}"

def select_lecture_query(fk) -> str:
    return \
        f"SELECT * FROM private.lecture WHERE fk = {fk}"

def select_material_query(fk) -> str:
    return \
        f"SELECT * FROM private.video "


def get_grade_by_name_query(grade_name) -> str:
    if filter(grade_name):
        return \
            f"SELECT * FROM private.grade WHERE name_en = '{grade_name}'"
    else:
        warn_injection()
        return None

def get_subject_by_name_query(fk, subject_name) -> str:
    if filter(f"{fk} {subject_name}"):
        return \
            f"SELECT * FROM private.subject WHERE name_en = '{subject_name}' AND fk = {fk}"
    else:
        warn_injection()
        return None

def get_branch_by_name_query(fk, branch_name) -> str:
    if filter(f"{fk} {branch_name}"):
        return \
            f"SELECT * FROM private.branch WHERE name_en = '{branch_name}' AND fk = {fk}"
    else:
        warn_injection()
        return None

def get_lecture_by_name_query(fk, lecture_name) -> str:
    if filter(f"{fk} {lecture_name}"):
        return \
            f"SELECT * FROM private.lecture WHERE name_en = '{lecture_name}' AND fk = {fk}"
    else:
        warn_injection()
        return None

# material queries
def slecet_material_query(fk, material_type) -> str:
    return \
        f"SELCT * FROM private.{material_type} WHERE fk = {fk}"

def select_material_parts(fk, material_type, part_type) -> str:
    return \
        f"SELECT * FROM private.{material_type}_{part_type} WHERE fk = {fk}"


