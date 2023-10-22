import pyodbc
import requests
import json
import time
import logging

# Создание объекта logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Подключение к базе данных MS SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=your_server;'
                      'Database=your_database;'
                      'UID=your_username;'
                      'PWD=your_password;')
logger.info('Подключение к базе данных')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Запрос к базе данных для получения всех IP-адресов из таблицы ESP_IP
cursor.execute("SELECT ip_address FROM ESP_IP")

# Получение всех IP-адресов
ip_addresses = [row.ip_address for row in cursor.fetchall()]

while ip_addresses:
    # Извлечение IP-адреса из списка
    ip_address = ip_addresses.pop(0)

    # Выполнение HTTP-запроса к устройству
    response = requests.get(f'http://{ip_address}/sensor_data')

    # Проверка статуса ответа
    if response.status_code == 200:
        # Получение данных сенсоров из ответа
        sensor_data = response.json()

        # Запись данных сенсоров в базу данных
        query = f"INSERT INTO ESP_Data (Sensor1, Sensor2, Sensor3) VALUES ({sensor_data['Sensor1']}, {sensor_data['Sensor2']}, {sensor_data['Sensor3']})"
        cursor.execute(query)
        logger.info('Данные сенсоров записаны в базу данных')
    # Задержка в 5 секунд перед следующим запросом
    time.sleep(5)

# Закрытие соединения с базой данных
conn.close()
logger.info('Соединение с базой данных закрыто')
