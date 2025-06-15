import json

from werkzeug.security import generate_password_hash, check_password_hash
from requests import get, post, delete, put


def test_get_user(type_test, ip, port, user_id=None):
    if not user_id:
        print(json.dumps(get(f'http://{ip}:{port}/api/{type_test}/users').json(), indent=4, ensure_ascii=False))
    else:
        print(json.dumps(get(f'http://{ip}:{port}/api/{type_test}/users/{user_id}').json(), indent=4, ensure_ascii=False))


def test_add_user(type_test, ip, port, json_f):
    print(
        f'Добавление {json_f}...\n',
        post(f'http://{ip}:{port}/api/{type_test}/users', json=json_f).json()
    )


def test_delete_user(type_test, ip, port, user_id):
    print(
        f'Было до удаления:\n',
        get(f'http://{ip}:{port}/api/{type_test}/users').json()
    )
    response = delete(f'http://{ip}:{port}/api/{type_test}/users/{user_id}')
    print(
        '\nРезультат удаления:\n',
        response.json()
    )

    if not ('error' in response.json().keys()):
        print(
            f'\nСтало после удаления:\n',
            get(f'http://{ip}:{port}/api/{type_test}/users').json()
        )


def test_edit_user(type_test, ip, port, user_id, json_f):
    print(
        f'Было до редактирования:\n',
        get(f'http://{ip}:{port}/api/{type_test}/users').json()
    )

    response = put(f'http://{ip}:{port}/api/{type_test}/users/{user_id}', json=json_f)
    print(
        '\nРезультат изменения:\n',
        response.json()
    )

    if not ('error' in response.json().keys()):
        print(
            f'\nСтало после редактирования:\n',
            get(f'http://{ip}:{port}/api/{type_test}/users/{user_id}').json()
        )


my_little_password = '12334478272'
hashed_passwd = generate_password_hash(my_little_password)

test_json = {
    'surname': '',
    'name': '',
    'nickname': '',
    'age': 20,
    'country': '',
    'email': '',
    'user_photo': '',
    'hashed_password': hashed_passwd
}


test_get_user('v2', 'localhost', '5000')
