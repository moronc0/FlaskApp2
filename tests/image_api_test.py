import json
from requests import get, post, delete, put


def test_get_image(type_test, ip, port, image_id=None):
    if not image_id:
        print(json.dumps(get(f'http://{ip}:{port}/api/{type_test}/images').json(), indent=4, ensure_ascii=False))
    else:
        print(
            json.dumps(get(f'http://{ip}:{port}/api/{type_test}/images/{image_id}').json(), indent=4, ensure_ascii=False))


def test_add_image(type_test, ip, port, json_f):
    print(
        f'Добавление {json_f}...\n',
        post(f'http://{ip}:{port}/api/{type_test}/images', json=json_f).json()
    )


def test_delete_image(type_test, ip, port, image_id):
    print(
        f'Было до удаления:\n',
        get(f'http://{ip}:{port}/api/{type_test}/images').json()
    )
    response = delete(f'http://{ip}:{port}/api/{type_test}/images/{image_id}')
    print(
        '\nРезультат удаления:\n',
        response.json()
    )

    if not ('error' in response.json().keys()):
        print(
            f'\nСтало после удаления:\n',
            get(f'http://{ip}:{port}/api/{type_test}/images').json()
        )


def test_edit_image(type_test, ip, port, image_id, json_f):
    print(
        f'Было до редактирования:\n',
        get(f'http://{ip}:{port}/api/{type_test}/images').json()
    )

    response = put(f'http://{ip}:{port}/api/{type_test}/images/{image_id}', json=json_f)
    print(
        '\nРезультат изменения:\n',
        response.json()
    )

    if not ('error' in response.json().keys()):
        print(
            f'\nСтало после редактирования:\n',
            get(f'http://{ip}:{port}/api/{type_test}/images/{image_id}').json()
        )


test_json = {
    'title': 'test',
    'about': 'test',
    'owner': 1,
    'tags': '2',
    'image_name': 'root/root_something.png'
}

test_delete_image('v1', 'localhost', '5000', 11)
