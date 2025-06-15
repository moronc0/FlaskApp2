from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField
from wtforms.fields.simple import TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Regexp


class AddImagesForm(FlaskForm):
    title = StringField('Название изображения', validators=[DataRequired()])
    about = TextAreaField('Описание изображения')
    tags = StringField('Тэги', validators=[DataRequired(), Regexp(r'^[A-Za-zА-Яа-яёЁ0-9\s\-,]+$')])
    image = FileField('Изображение', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'],
                                                                             'Только изображения!')])
    submit = SubmitField('Добавить')

