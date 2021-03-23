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
