def select_material_query(table) -> str:
    return \
        f"SELECT (public.select_{table}()).*"
# material parts
def select_material_parts_query(presentation, media_type) -> str:
    return \
        f"SELECT (public.select_{presentation}_{media_type}()).*"


def select_about_us_query() -> str:
    return \
        f"SELECT (public.select_about_us()).*"

def select_instruction_query() -> str:
    return \
        f"SELECT (public.select_instruction()).*"

def select_faq_query(offset=0, limit=None) -> str:
    if not limit:
        limit = 'null'
    return \
        f"SELECT (public.select_faq({offset}, {limit})).*"