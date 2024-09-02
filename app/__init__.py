import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание объектов расширений
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    """Функция для создания и настройки экземпляра Flask приложения."""
    # Загрузка переменных окружения
    load_dotenv()

    app = Flask(__name__)

    # Загрузка конфигурации из переменных окружения
    try:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        if app.config['SECRET_KEY'] is None:
            raise ValueError("SECRET_KEY не найден в переменных окружения.")

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/shrio/PycharmProjects/UAV_final/instance/users.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        """
        SQLALCHEMY_TRACK_MODIFICATIONS установлена в `False` для отключения функции отслеживания изменений объектов, 
        которая не используется и может замедлять приложение.
        """

        logger.info("Конфигурация приложения загружена успешно.")
    except Exception as e:
        logger.error("Ошибка при загрузке конфигурации приложения: %s", e)
        raise

    # Подключение расширений
    try:
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)

        login_manager.login_view = 'login'
        logger.info("Расширения Flask инициализированы успешно.")
    except Exception as e:
        logger.error("Ошибка при инициализации расширений: %s", e)
        raise

    with app.app_context():
        # Импорт моделей и создание таблиц
        from .models import User
        db.create_all()
        """
        вызов `db.create_all()` внутри контекста приложения (`app.app_context()`), 
        чтобы гарантировать создание таблиц в базе данных при инициализации приложения.
        """
        logger.info("Таблицы базы данных созданы.")

    return app

# Инициализация приложения
app = create_app()

# Импортировать модули маршрутов в конце, чтобы избежать проблем с циклическими импортами
from app import routes

