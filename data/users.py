import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from data.db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Users(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    serialize_only = (
        'id',
        'surname',
        'name',
        'nickname',
        'age',
        'country',
        'email',
        'user_photo'
    )

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )

    surname = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        info={
            'description': 'Фамилия'
        }
    )

    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        info={
            'description': 'Имя'
        }
    )

    nickname = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True,
        info={
            'description': 'Никнейм'
        }
    )

    age = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        info={
            'description': 'Возраст'
        }
    )

    country = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True,
        info={
            'description': 'Страна'
        }
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False,
        info={
            'description': 'Почта'
        }
    )
    hashed_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        info={
            'description': 'Хэш пароль'
        }
    )

    user_photo = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True,
        info={
            'description': 'Фото пользователя'
        }
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    images = orm.relationship('Images', back_populates='user')
