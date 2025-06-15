from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField
from wtforms.fields.simple import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Regexp, Optional


class EditImageForm(FlaskForm):
    title = StringField('Название изображения', validators=[DataRequired()])
    about = TextAreaField('Описание изображения')
    tags = StringField('Тэги', validators=[DataRequired(), Regexp(r'^[A-Za-zА-Яа-яёЁ0-9\s,-]+$')])
    image = FileField('Новое изображение (не обязательно)',
                      validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
    submit = SubmitField('Сохранить изменения')
