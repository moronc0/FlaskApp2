import pycountry

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, NumberRange, Optional, Email, Length, EqualTo


def get_countries():
    countries = [(None, 'Не указано')]
    countries += [(country.alpha_2, country.name) for country in pycountry.countries]
    return countries


class RegisterUserForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired(), Regexp(r'^[A-Za-zА-Яа-яёЁ\s-]+$')])
    name = StringField('Имя', validators=[DataRequired(), Regexp(r'^[A-Za-zА-Яа-яёЁ\s-]+$')])
    nickname = StringField('Никнейм', validators=[DataRequired(), Regexp(r'^[A-Za-z_]+$')])
    age = IntegerField('Возраст', validators=[DataRequired(), NumberRange(min=16, max=120, message='От 16 лет')])
    country = SelectField('Страна', choices=get_countries(), default=None, validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message="Пароль обязателен"),
            Length(min=8, message="Пароль должен быть не менее 8 символов")
        ]
    )

    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(message="Повторите пароль"),
            EqualTo('password', message="Пароли должны совпадать")
        ]
    )
    image = FileField('Изображение', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'],
                                                                             'Только изображения!')])

    submit = SubmitField('Зарегистрироваться')
