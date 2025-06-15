import os
import shutil

from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import Users
from parsers import users_parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(Users).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)

        return jsonify(
            {
                'user': user.to_dict()
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)

        session.delete(user)
        session.commit()

        user_dir = os.path.join('static', user.nickname)
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)

        session.close()

        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()

        return jsonify(
            {
                'users':
                    [item.to_dict() for item in users]
            }
        )

    def post(self):
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
