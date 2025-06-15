import os.path
from datetime import datetime

from flask import render_template, redirect, Flask, make_response, jsonify, url_for, request
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload

from blueprint_api import images_api, users_api
from forms.login_form import LoginUserForm
from forms.register_user_form import RegisterUserForm
from forms.add_image_form import AddImagesForm
from forms.edit_image_form import EditImageForm
from data.users import Users
from data.images import Images
from data import db_session
from resources import users_resource, images_resource

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/gallery')
def gallery():
    session = db_session.create_session()
    query = session.query(Images).options(joinedload(Images.user))

    author = request.args.get('author', '').strip()
    tag = request.args.get('tag', '').strip()

    if author:
        query = query.join(Images.user).filter(Users.nickname.ilike(f"%{author}%"))
    if tag:
        query = query.filter(Images.tags.contains([tag]))

    images = query.all()
    session.close()
    return render_template('gallery.html', images=images)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginUserForm()
    if login_form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(Users).filter(Users.email == login_form.email.data).first()

        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)

            return redirect(f'/profile/id/{user.id}')

        return render_template('login.html', title='Авторизация',
                               message="Неправильный логин или пароль",
                               form=login_form)
    return render_template('login.html', title='Авторизация', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterUserForm()
    if register_form.validate_on_submit():
        session = db_session.create_session()

        if session.query(Users).filter(Users.nickname == register_form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=register_form,
                                   message='Пользователь с таким никнеймом уже существует')

        if session.query(Users).filter(Users.email == register_form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=register_form,
                                   message='Пользователь с таким email уже существует')

        file = register_form.image.data
        user_dir = os.path.join('static', register_form.nickname.data)
        os.makedirs(user_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{register_form.nickname.data}_profile_{timestamp}{os.path.splitext(file.filename)[1]}'
        file_path = os.path.join(user_dir, filename)
        file.save(file_path)

        user = Users(
            surname=register_form.surname.data,
            name=register_form.name.data,
            nickname=register_form.nickname.data,
            age=register_form.age.data,
            country=register_form.country.data,
            email=register_form.email.data,
            user_photo=f'{register_form.nickname.data}/{filename}'
        )
        user.set_password(register_form.password.data)

        session.add(user)
        session.commit()

        login_user(user)

        session.close()
        return redirect(f'/profile/id/{user.id}')
    return render_template('register.html', title='Регистрация', form=register_form)


@login_required
@app.route('/profile/id/<int:id>', methods=['GET', 'POST'])
def show_profile(id):
    session = db_session.create_session()
    user = session.query(Users).get(id)
    if not user:
        return make_response('No such profile', 404)
    images = session.query(Images).filter(Images.owner == user.id).all()

    params = {
        'title': 'Профиль',
        'nickname': user.nickname,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
        'country': user.country,
        'user_photo': user.user_photo,
        'images': images,
        'is_own_profile': current_user.id == user.id,
        'user': user
    }

    session.close()
    return render_template('profile.html', **params)


@login_required
@app.route('/image_add', methods=['GET', 'POST'])
def add_image():
    if not (current_user.id == 1 or current_user.id == int(request.args.get('user_id', current_user.id))):
        return make_response('No access', 404)
    image_form = AddImagesForm()
    if image_form.validate_on_submit():
        session = db_session.create_session()

        file = image_form.image.data

        user_dir = os.path.join('static', current_user.nickname)
        os.makedirs(user_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'{current_user.nickname}_{timestamp}{os.path.splitext(file.filename)[1]}'

        file_path = os.path.join(user_dir, filename)
        file.save(file_path)

        images = Images(
            title=image_form.title.data,
            about=image_form.about.data,
            owner=current_user.id,
            tags=image_form.tags.data.split(','),
            image_name=f'{current_user.nickname}/{filename}'
        )

        current_user.images.append(images)
        session.merge(current_user)
        session.commit()
        session.close()

        return redirect(f'/profile/id/{current_user.id}')
    return render_template('images_add.html', title='Добавление изображения',
                           form=image_form)


@app.route('/image_delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    session = db_session.create_session()
    image = session.query(Images).get(image_id)
    if not image or not (current_user.id == 1 or current_user.id == image.owner):
        return redirect(url_for('show_profile', id=current_user.id))
    image_path = os.path.join('static', image.image_name)
    if os.path.exists(image_path):
        os.remove(image_path)
    session.delete(image)
    session.commit()
    session.close()
    return redirect(url_for('show_profile', id=current_user.id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


#       АДМИНСКОЕ
@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def show_admin_panel():
    if current_user.id != 1:
        return redirect(url_for('show_profile', id=current_user.id))

    session = db_session.create_session()
    users = session.query(Users).all()
    params = {
        'title': 'Панель админа',
        'users': users
    }

    session.close()
    return render_template('admin_panel.html', **params)


@app.route('/image_edit/<int:image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    session = db_session.create_session()
    image = session.query(Images).get(image_id)
    if not image or not (current_user.id == 1 or current_user.id == image.owner):
        session.close()
        return redirect(url_for('show_profile', id=current_user.id))

    form = EditImageForm(obj=image)
    if form.validate_on_submit():
        image.title = form.title.data
        image.about = form.about.data
        image.tags = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        if form.image.data:
            old_image_path = os.path.join('static', image.image_name)
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
            file = form.image.data
            user_dir = os.path.join('static', current_user.nickname)
            os.makedirs(user_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'{current_user.nickname}_{timestamp}{os.path.splitext(file.filename)[1]}'
            file_path = os.path.join(user_dir, filename)
            file.save(file_path)
            image.image_name = f'{current_user.nickname}/{filename}'
        session.commit()
        session.close()
        return redirect(url_for('show_profile', id=current_user.id))
    if request.method == 'GET':
        form.tags.data = ', '.join(image.tags) if image.tags else ''
    session.close()
    return render_template('edit_image.html', form=form, image=image)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init(f'db/sem.db')

    app.register_blueprint(images_api.blueprint)
    app.register_blueprint(users_api.blueprint)

    api.add_resource(images_resource.ImageListResource, '/api/v2/images')
    api.add_resource(images_resource.ImageResource, '/api/v2/images/<int:image_id>')

    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(users_resource.UserListResource, '/api/v2/users')

    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()
