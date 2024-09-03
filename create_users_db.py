import os
from admin_panel import create_app, db, bcrypt
from admin_panel.models import User

def hash_password(password):
    # Хеширование пароля с использованием flask_bcrypt
    return bcrypt.generate_password_hash(password).decode('utf-8')

def create_db():
    app = create_app()

    # Убедитесь, что директория instance существует внутри admin_panel
    instance_path = os.path.join(app.root_path, 'instance')

    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    # Установите путь к базе данных в админ панели
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "users.db")}'

    with app.app_context():
        # Создание всех таблиц
        db.create_all()

        # Добавление первого пользователя-администратора, если он не существует
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            hashed_password = hash_password('SitkaCharlie273')  # Замените 'SitkaCharlie273' на ваш пароль
            admin_user = User(
                username='admin',
                email='shrion@yandex.ru',
                password=hashed_password,
                role='Admin',
                status='Active'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Пользователь-администратор успешно добавлен.")
        else:
            print("Пользователь-администратор уже существует.")

if __name__ == "__main__":
    create_db()
