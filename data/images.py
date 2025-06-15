from datetime import datetime

import sqlalchemy

from data.db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Images(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'images'

    serialize_only = (
        'id',
        'title',
        'about',
        'owner',
        'tags',
        'image_name'
    )

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )

    title = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        info={
            'description': 'Название'
        }
    )

    about = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True,
        info={
            'description': 'Описание'
        }
    )

    owner = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=False
    )

    tags = sqlalchemy.Column(
        sqlalchemy.JSON,
        nullable=False,
        info={
            'description': 'Тэги'
        }
    )

    image_name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        info={
            'description': 'Название фото'
        }
    )

    edit_time = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.now,
        nullable=False,
        info={
            'description': 'Дата изменения'
        }
    )

    user = orm.relationship('Users', back_populates='images')
