import os
from admin_panel import create_app, db, bcrypt
from admin_panel.models import User
from .utils import create_instance_folder  # Импортируем функцию из utils.py


def hash_password(password):
    # Хеширование пароля с использованием flask_bcrypt
    return bcrypt.generate_password_hash(password).decode('utf-8')

def create_db():
    app = create_app()

    # Создаем папку instance
    create_instance_folder(app)

    # Убедитесь, что директория instance существует внутри admin_panel
    instance_path = os.path.join(app.root_path, 'instance')

    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    # Установите путь к базе данных в админ панели
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "users.db")}'

    with app.app_context():
        if not db.engine.connect().connection.execute(
                'SELECT name FROM sqlite_master WHERE type="table" AND name="user";').fetchone():
            db.create_all()

            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                hashed_password = hash_password('SitkaCharlie273')
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