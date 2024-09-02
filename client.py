import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# Определяем базовый URL для взаимодействия с сервером дронов
BASE_URL = 'http://localhost:5000'

def takeoff(drone_id, altitude, token):
    """
    Функция для отправки команды взлета дрону.

    :param drone_id: идентификатор дрона, которому отправляется команда взлета
    :param altitude: высота, на которую должен подняться дрон
    :return: ответ сервера в формате JSON
    """
    # Формируем URL для отправки команды взлета
    url = f"{BASE_URL}/drones/{drone_id}/takeoff"
    # Формируем полезную нагрузку с параметром высоты
    payload = {'altitude': altitude}
    headers = {'Authorization': f'Bearer {token}'}
    # Отправляем POST-запрос с полезной нагрузкой в формате JSON
    response = requests.post(url, json=payload, headers=headers)
    # Возвращаем ответ сервера в формате JSON
    return response.json()

def login(username, password):
    response = requests.post(f"{BASE_URL}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        logging.info(f"Пользователь {username} авторизирован!")
        return response.json().get('token')
    elif response.status_code == 403:
        print(f"Пользователь {username} не авторизирован!!!")
    return None

def register(username, password):
    response = requests.post(f"{BASE_URL}/register", json={'username': username, 'password': password})
    if response.status_code == 201:
        logging.info(f"Пользователь {username} зарегистрирован!")
    elif response.status_code == 400:
        print(f"Пользователь {username} уже зарегистрирован!!!")


if __name__ == '__main__':
    username = "EgorMv"
    password = "qwerty"
    register(username, password)
    token = login(username, password)
    if token:
        # Определяем идентификатор дрона
        drone_id = "drone_index"
        # Задаем высоту для взлета дрона
        altitude = 200

        # Вызываем функцию взлета и получаем ответ сервера
        response = takeoff(drone_id, altitude, token)
        # Выводим сообщение от сервера
        print(f"Ответ сервера: {response.get('message')}")
    else:
        print("Не смогли авторизироваться")
