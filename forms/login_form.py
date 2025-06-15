from flask_wtf import FlaskForm
from wtforms.fields.simple import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginUserForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


'''
<p class="mt-3">
    Нет аккаунта? <a href="{{ url_for('register') }}" class="btn btn-link">Создать аккаунт</a>
</p>
'''