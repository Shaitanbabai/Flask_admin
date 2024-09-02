import bcrypt
from app import create_app, db
from app.models import User


# def hash_password(password):
#     # Генерация соли и хэширование пароля
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed
#
#
# def create_db():
#     app = create_app()
#
#     with app.app_context():
#         # Создание всех таблиц
#         db.create_all()
#
#         # Добавление первого пользователя-администратора, если он не существует
#         admin_user = User.query.filter_by(username='admin').first()
#         if not admin_user:
#             hashed_password = hash_password('admin_password')  # Замените 'admin_password' на ваш пароль
#             admin_user = User(
#                 username='admin',
#                 email='admin@example.com',
#                 password=hashed_password,
#                 role='Admin',
#                 status='Active'
#             )
#             db.session.add(admin_user)
#             db.session.commit()
#         else:
#             print("Пользователь-администратор уже существует.")
#
#
# if __name__ == "__main__":
#     create_db()
