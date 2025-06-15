import os
import shutil

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import Users
from parsers import users_parser


blueprint = Blueprint('users_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/v1/users')
def get_users():
    session = db_session.create_session()
    users = session.query(Users).all()
    session.close()
    return jsonify(
        {
            'users':
                [item.to_dict() for item in users]
        }
    )


@blueprint.route('/api/v1/users/<int:user_id>')
def get_one_user(user_id):
    session = db_session.create_session()
    users = session.query(Users).get(user_id)

    session.close()

    if not users:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'user': users.to_dict()
        }
    )


@blueprint.route('/api/v1/users/', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})

    args = users_parser.parser.parse_args()
    session = db_session.create_session()

    hashed_password = generate_password_hash(args['password'])

    user = Users(
        surname=args['surname'],
        name=args['name'],
        nickname=args['nickname'],
        age=args['age'],
        country=args.get('country'),
        email=args['email'],
        hashed_password=hashed_password,
        user_photo=args.get('user_photo')
    )

    session.add(user)
    session.commit()
    session.close()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        session.close()
        return jsonify({'error': 'Not found'})

    session.delete(user)
    session.commit()

    user_dir = os.path.join('static', user.nickname)
    if os.path.exists(user_dir):
        shutil.rmtree(user_dir)

    session.close()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    args = users_parser.parser.parse_args()
    session = db_session.create_session()
    user = session.query(Users).get(user_id)

    hashed_password = generate_password_hash(args['password'])

    user.surname = args['surname']
    user.name = args['name']
    user.nickname = args['nickname']
    user.age = args['age']
    user.country = args.get('country')
    user.email = args['email']
    user.hashed_password = hashed_password
    user.user_photo = args.get('user_photo')

    session.commit()
    session.close()

    return jsonify({'success': 'OK'})
