import requests
from flask import Flask, Response, request, jsonify

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Определяем базовый URL для взаимодействия с сервером дронов
BASE_URL = 'http://127.0.0.1:5000/drones'

# Инициализируем словарь с информацией о дроне
drone = {
    "drone_index": {
        "model": "DJI Phantom",
        "battery": 100,
        "control_url": "http://127.0.0.1:5001"
    }
}

@app.route("/takeoff", methods=["POST"])
def takeoff():
    """
    Обрабатываем запрос на взлет дрона.

    :return: JSON-ответ с сообщением о результате взлета
    """
    # Получаем высоту из запроса
    altitude = request.json.get('altitude')
    # Логика взлета (здесь просто выводим сообщение в консоль)
    print(f"Взлетаем на высоту: {altitude} метров")
    # Возвращаем JSON-ответ с сообщением
    return jsonify({"message": f"Взлет на высоту {altitude} метров выполнен"}), 200

def register_drone(drone_id, drone_info):
    """
    Регистрируем дрон на сервере.

    :param drone_id: идентификатор дрона
    :param drone_info: информация о дроне
    :return: ответ сервера в формате JSON
    """
    # Формируем URL для регистрации дрона
    url = BASE_URL
    # Формируем полезную нагрузку с информацией о дроне
    payload = {
        'drone_id': drone_id,
        **drone_info
    }
    # Отправляем POST-запрос с полезной нагрузкой в формате JSON
    response = requests.post(url, json=payload)
    # Возвращаем ответ сервера в формате JSON
    return response.json()

if __name__ == '__main__':
    # Определяем идентификатор дрона
    drone_id = "drone_index"
    # Получаем информацию о дроне из словаря
    drone_info = drone[drone_id]
    # Регистрируем дрон на сервере и получаем ответ
    response = register_drone(drone_id, drone_info)
    # Выводим сообщение о регистрации дрона
    print(f"Регистрация дрона: {response.get('message')}")
    # Запускаем Flask сервер на порту 5001
    # На ПК иногда параноидальная система безопасности и
    # может блокировать популярные порты, например 8080
    app.run(host='0.0.0.0', port=5001, debug=True)

    # Исправление ошибки, если Drone запускается на порту 5000
    # через терминал запускаем flask
    # python -m flask --admin_panel "ПУТЬ_ДО_ФАЙЛА" run --port=5001

    # python -m flask --admin_panel "drone.py" run --port=5001
