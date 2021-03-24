from app.db.repositories.filter import filter, warn_injection

def select_grades_query(ids=[]) -> str:
    if ids:
        available = str(ids).strip('[ ]')
        return \
            f"SELECT * FROM private.grade WHERE id IN ({available})"
    else:
        return \
            f"SELECT * FROM private.grade"

def select_subject_query(fk, ids=[]) -> str:
    if ids:
        available = str(ids).strip('[ ]')
        return \
            f"SELECT * FROM private.subject WHERE id IN ({available}) AND fk = {fk}"
    else:
        return \
            f"SELECT * FROM private.subject WHERE fk = {fk}"

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

