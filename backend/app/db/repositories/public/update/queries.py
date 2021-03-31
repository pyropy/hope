from app.db.repositories.parsers import string_or_null

def update_video_query(name_ru, url, description) -> str:
    return \
        f"SELECT (public.update_video({string_or_null(name_ru, url, description)})).*"

def update_game_query(name_ru, url, description) -> str:
    return \
        f"SELECT (public.update_game({string_or_null(name_ru, url, description)})).*"

def update_about_us_query(order_number, title, description, svg) -> str:
    return \
        f"SELECT (public.update_about_us({order_number}, {string_or_null(title, description, svg)})).*"


def update_instruction_query(order_number, title, description) -> str:
    return \
        f"SELECT (public.update_instruction({order_number}, {string_or_null(title, description)})).*"

def update_faq_query(id, question, answer) -> str:
    return \
        f"SELECT (public.update_faq({id}, {string_or_null(question, answer)})).*"
