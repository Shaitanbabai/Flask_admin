import logging
from admin_panel import login_manager, db
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from abc import ABC, abstractmethod

# Создаем экземпляр MetaData с параметром extend_existing=True
metadata = MetaData()

# Инициализация SQLAlchemy с использованием настроенного MetaData
# db = SQLAlchemy()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.get(int(user_id))
        if user:
            logging.info(f'User loaded: {user.username}')
        else:
            logging.warning(f'User with id {user_id} not found.')
        return user
    except Exception as e:
        logging.error(f'Error loading user with id {user_id}: {e}')
        return None



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='User')
    status = db.Column(db.String(10), nullable=False, default='Inactive')

    def __init__(self, username, email, password, role='User', status='Inactive'):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.status = status
        logging.info(f'User created: {self.username}, role: {self.role}, status: {self.status}')

    def __repr__(self):
        return f'User: {self.username}, email: {self.email}, role: {self.role}, status: {self.status}'

class UserFactory(ABC):
    @abstractmethod
    def create_user(self, username, email, password):
        pass

class AdminFactory(UserFactory):
    def create_user(self, username, email, password):
        try:
            user = User(username, email, password, role='Admin')
            logging.info(f'Admin user created: {user.username}')
            return user
        except Exception as e:
            logging.error(f'Error creating admin user: {e}')
            return None

class StandardUserFactory(UserFactory):
    def create_user(self, username, email, password):
        try:
            user = User(username, email, password, role='User')
            logging.info(f'Standard user created: {user.username}')
            return user
        except Exception as e:
            logging.error(f'Error creating standard user: {e}')
            return None

class UserStatusFactory(ABC):
    @abstractmethod
    def set_status(self, user):
        pass

class ActiveStatusFactory(UserStatusFactory):
    def set_status(self, user):
        try:
            user.status = 'Active'
            logging.info(f'Status set to Active for user: {user.username}')
            return user
        except Exception as e:
            logging.error(f'Error setting status to Active for user {user.username}: {e}')
            return None

class InactiveStatusFactory(UserStatusFactory):
    def set_status(self, user):
        try:
            user.status = 'Inactive'
            logging.info(f'Status set to Inactive for user: {user.username}')
            return user
        except Exception as e:
            logging.error(f'Error setting status to Inactive for user {user.username}: {e}')
            return None
