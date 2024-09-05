import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from admin_panel.utils import create_instance_folder

# Загрузка переменных окружения
load_dotenv()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание объектов расширений
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

class Config:
    """Конфигурация приложения."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    """Функция для создания и настройки экземпляра Flask приложения."""
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(Config)

    if not flask_app.config['SECRET_KEY']:
        logger.error("SECRET_KEY не найден в переменных окружения.")
        raise ValueError("SECRET_KEY не найден в переменных окружения.")

    # Проверка и создание instance_path
    try:
        if not os.path.exists(flask_app.instance_path):
            os.makedirs(flask_app.instance_path)
            logger.info("Создан instance_path: %s", flask_app.instance_path)
    except OSError as error:
        logger.error("Ошибка при создании instance_path: %s", error)
        raise

    # Подключение расширений
    try:
        db.init_app(flask_app)
        bcrypt.init_app(flask_app)
        login_manager.init_app(flask_app)

        login_manager.login_view = 'main.login'
        logger.info("Расширения Flask инициализированы успешно.")
    except Exception as error:
        logger.error("Ошибка при инициализации расширений: %s", error)
        raise

    # Импортировать модули маршрутов
    try:
        from admin_panel.routes import main as main_blueprint
        flask_app.register_blueprint(main_blueprint)
        logger.info("Маршруты зарегистрированы.")
    except ImportError as error:
        logger.error("Ошибка при импорте маршрутов: %s", error)
        raise

    create_instance_folder(flask_app)

    return flask_app


# Инициализация приложения
app = create_app()


"""
SQLALCHEMY_TRACK_MODIFICATIONS установлена в `False` для отключения функции отслеживания изменений объектов,
которая не используется и может замедлять приложение.
"""

"""
вызов `db.create_all()` внутри контекста приложения (`admin_panel.app_context()`),
чтобы гарантировать создание таблиц в базе данных при инициализации приложения.
"""

