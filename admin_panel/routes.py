from flask import Blueprint, jsonify, request, render_template, abort, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from admin_panel import db, bcrypt
from admin_panel.models import User
from admin_panel.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateUserForm
from functools import wraps


# Создаем Blueprint
main = Blueprint('main', __name__)

# Декоратор для ограничения доступа только для администраторов
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin' or current_user.status != 'Active':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main.errorhandler(403)
def access_denied(e):
    return render_template('403.html', message="Access denied", user=current_user), 403

# Главная страница
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

# Регистрация пользователя с установкой статуса по умолчанию как 'Inactive'
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Захешируем пароль
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Проверяем, есть ли уже пользователи в базе данных
        if User.query.count() == 0:
            # Первый пользователь становится администратором и активным
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                role='Admin',
                status='Active'
            )
            flash('Первый пользователь зарегистрирован как администратор.', 'success')
        else:
            # Все остальные пользователи — обычные юзеры с неактивным статусом
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                role='User',
                status='Inactive'
            )
            flash('Вы успешно зарегистрировались. Дождитесь активации администратором.', 'success')

        # Сохраняем пользователя в базу данных
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# Вход в аккаунт
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Введены неверные данные', 'danger')

    return render_template('login.html', form=form)

# Выход из аккаунта
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Страница аккаунта
@main.route('/account')
@login_required
def account():
    user = User.query.get(current_user.id)
    return render_template('account.html', user=user)

# Редактирование аккаунта
@main.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('main.edit_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_account.html', form=form)

# Список пользователей (доступно только администраторам)
@main.route("/users", methods=["GET", "POST"])
@admin_required
@login_required
def list_users():
    users = User.query.all()
    if request.method == "POST":
        user_id = request.form.get("user_id")
        role = request.form.get("role")
        status = request.form.get("status")
        user = User.query.get(user_id)
        if user:
            user.role = role
            user.status = status
            db.session.commit()
            flash('Информация о пользователе обновлена', 'success')
        return redirect(url_for('main.list_users'))
    return render_template("users.html", users=users)

# Обновление информации о пользователе (доступно только администраторам)
@main.route("/user/<int:user_id>/update", methods=["POST", "PUT"])
@admin_required
@login_required
def update_user(user_id):
    """Обновление информации о пользователе, доступно только администраторам."""
    user = User.query.get_or_404(user_id)
    data = request.get_json()  # Теперь используем get_json для получения данных

    role = data.get('role')
    status = data.get('status')

    if role:
        user.role = role
    if status:
        user.status = status

    db.session.commit()
    flash('Информация о пользователе обновлена', 'success')
    return jsonify({"success": True}), 200
