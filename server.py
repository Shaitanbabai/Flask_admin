import requests
from flask import Flask, Response, request, jsonify
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)

# Определение маршрутов и операций для управления дронами и полетами
# Комментарии включают объяснение каждого маршрута и его функций

# Управление дронами

# GET
# /drones - Получить список всех дронов
# /drones/{drone_id} - Получить информацию о конкретном дроне

# POST
# /drones - Создать нового дрона

# PUT
# /drones/{drone_id} - Обновить информацию о конкретном дроне

# DELETE
# /drones/{drone_id} - Удалить конкретного дрона

# Управление полетом

# POST
# /drones/{drone_id}/takeoff - Команда взлета дрона
# /drones/{drone_id}/land - Команда посадки дрона
# /drones/{drone_id}/move - Команда перемещения дрона

# GET
# /drones/{drone_id}/sensors - Получить данные сенсоров дрона

# Пример взлета
# POST /drones/{drone_id}/takeoff
# {
#     "altitude": 10
# }

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Конфигурируем секретный ключ для JWT
app.config['SECRET_KEY'] = 'my_secret_key'
# Инициализируем менеджер JWT для управления токенами
my_jwt = JWTManager(app)

# Инициализируем словарь для хранения информации о дронах
drones = {}

# Инициализируем словарь для хранения информации о пользователях
users = {}

@app.route("/register", methods=["POST"])
def register():
    """
    Регистрация нового пользователя.

    :return: JSON-ответ с сообщением об успешной регистрации и статус-код 201,
             или ошибка 400, если пользователь уже существует
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users:
        return jsonify({"error": "Пользователь уже существует"}), 400
    users[username] = password
    return jsonify({"message": "Успешно зарегистрировались"}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Авторизация пользователя и получение JWT-токена.

    :return: JSON-ответ с токеном и статус-код 200,
             или ошибка 403, если логин или пароль неверны
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if users.get(username) != password:
        return jsonify({"error": "Неверный логин или пароль"}), 403
    # Создаем токен доступа для авторизованного пользователя
    token = create_access_token(identity=username)
    return jsonify(token=token), 200


@app.route("/drones", methods=["GET"])
@jwt_required()
def get_drones():
    """
    Возвращает список всех дронов.

    :return: JSON-ответ со списком всех дронов и статус-код 200
    """
    return jsonify(drones), 200

@app.route("/drones/<drone_id>", methods=["GET"])
def get_drone(drone_id):
    """
    Возвращает информацию о конкретном дроне.

    :param drone_id: идентификатор дрона
    :return: JSON-ответ с информацией о дроне и статус-код 200,
             или ошибка 404, если дрон не найден
    """
    drone = drones.get(drone_id)
    if drone:
        return jsonify(drone), 200
    return jsonify({"error": "Дрон не найден"}), 404

@app.route("/drones", methods=["POST"])
def create_drone():
    """
    Создает нового дрона.

    :return: JSON-ответ с сообщением об успешном добавлении дрона и статус-код 201,
             или ошибка 404, если не передан id дрона
    """
    drone_id = request.json.get("drone_id")
    if drone_id:
        drones[drone_id] = request.json
        return jsonify({"message": f"Дрон {drone_id} добавлен"}), 201
    return jsonify({"error": "Не передан id дрона"}), 404

@app.route("/drones/<drone_id>/takeoff", methods=["POST"])
@jwt_required()
def takeoff_drone(drone_id):
    """
    Отправляет команду взлета конкретному дрону.

    :param drone_id: идентификатор дрона
    :return: JSON-ответ с сообщением об успешном взлете и статус-код 200,
             или ошибка 404, если дрон не зарегистрирован,
             или ошибка 500, если произошла ошибка при взлете
    """
    if drone_id not in drones:
        return jsonify({"error": f"Дрон c id: {drone_id} не зарегистрирован"}), 404
    altitude = request.json.get("altitude")
    drone_info = drones[drone_id]
    drone_url = drone_info["control_url"] + "/takeoff"
    # Отправляем запрос на взлет дрона к его управляющему URL
    response = requests.post(drone_url, json={"altitude": altitude})
    if response.status_code == 200:
        return jsonify({"message": response.json().get("message")}), 200
    return jsonify({"error": f"Ошибка взлета дрона id: {drone_id}"}), 500

if __name__ == '__main__':
    # Запускаем Flask сервер с отладкой
    app.run(debug=True)
