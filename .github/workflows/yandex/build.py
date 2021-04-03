import os
import json

YANDEX_ID = os.getenv('YANDEX_ID')
YANDEX_PUBLIC_KEY = os.getenv('YANDEX_PUBLIC_KEY')
YANDEX_KEY_ALGORITHM = os.getenv('YANDEX_KEY_ALGORITHM')
YANDEX_CREATED_AT = os.getenv('YANDEX_CREATED_AT')
YANDEX_SERVICE_ACCOUNT_ID = os.getenv('YANDEX_SERVICE_ACCOUNT_ID')
YANDEX_PRIVATE_KEY = os.getenv('YANDEX_PRIVATE_KEY')
YANDEX_REGISTRY_URL = os.getenv('YANDEX_REGISTRY_URL')

TAG = f'{YANDEX_REGISTRY_URL}/backend:latest'

def create_key():
    return {
        "id": YANDEX_ID,
        "service_account_id": YANDEX_SERVICE_ACCOUNT_ID,
        "created_at": YANDEX_CREATED_AT,
        "key_algorithm": YANDEX_KEY_ALGORITHM,
        "public_key": YANDEX_PUBLIC_KEY,
        "private_key": YANDEX_PRIVATE_KEY}

def authenticate():
    creds = create_key()
    json.dump(creds, open('key.json', 'w'))
    os.system(
    f'cat key.json | docker login ' \
    f'--username json_key ' \
    f'--password-stdin ' \
    f'cr.yandex'
    )
    os.system('rm key.json')

def build():
    os.system(f'docker build -t {TAG} ./backend')

def push():
    os.system(f'docker push {TAG}')

def main():
    authenticate()
    build()
    push()
    

if __name__ == "__main__":
    main()