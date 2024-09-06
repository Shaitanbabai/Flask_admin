import os
from admin_panel import create_app, db, bcrypt
from admin_panel.models import User


def hash_password(password):
    # Хеширование пароля с использованием flask_bcrypt
    return bcrypt.generate_password_hash(password).decode('utf-8')

def create_db():
    app = create_app()

    # Определяем путь к базе данных
    db_path = os.path.join(app.instance_path, 'users.db')
    # Конфигурируем SQLAlchemy с использованием db_path
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    # db.init_app(app)

    if not os.path.exists(db_path):  # Проверяем существование таблицы
        with app.app_context():
            # if not db.engine.connect().connection.execute(
            #         f"SELECT name FROM sqlite_master WHERE type='table' AND name='users';").fetchone():
           db.create_all()

                # Создание администратора
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            hashed_password = hash_password('MyFuckingSecretPassword')
            admin_user = User(
                    username='admin',
                    email='ex-hosted@yandex.ru',
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