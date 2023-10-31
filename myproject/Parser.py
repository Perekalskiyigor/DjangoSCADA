import pyodbc
import requests
import json
import time
from requests.exceptions import ConnectTimeout
from datetime import datetime


# Подключение к базе данных MS SQL Server
try:
       conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=10.11.21.24;'
                            'Database=BI_TEST;'
                            'UID=Perekalskiy_igor;'
                            'PWD=Fnkfynblf198714;')
except pyodbc.Error as ex:
       print("Ошибка подключения к базе данных: ", ex)
print('Подключение к базе данных успешно')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()
# Запрос к базе данных для получения всех IP-адресов из таблицы ESP_IP
cursor.execute("SELECT id, ip_address, Description FROM ESP_IP")
print ('Запрос на получение IP адресов: успешно')


# Получение всех IP-адресов
for row in cursor.fetchall():
    ip_address = row.ip_address
    description = row.Description
    id = row.id
    
    try:
        # Выполнение HTTP-запроса к устройству
        response = requests.get(f'http://{ip_address}/sensor_data')

        # Проверка статуса ответа
        if response.status_code == 200:
            # Получение данных сенсоров из ответа
            sensor_data = response.json()
            # Запись данных сенсоров в базу данных
            insert_query = "INSERT INTO ESPTable ([Data], [Description], [Status], Sensor1, Sensor2, Sensor3, Sensor4, Sensor5, Sensor6, ESP_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (formatted_time, description, '200', sensor_data['Sensor1'], sensor_data['Sensor2'], sensor_data['Sensor3'], sensor_data['Sensor4'], sensor_data['Sensor5'], sensor_data['Sensor6'], id )
            cursor.execute(insert_query, params)
            conn.commit()
            print('Данные сенсоров записаны в базу данных')
    except ConnectTimeout:
        # Получение текущего времени
        current_time = datetime.now()
        # Форматирование времени в формат 'YYYY-MM-DD HH:MM:SS'
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        print(formatted_time)
        try:
            # Запись статуса 404 и заполнение всех ячеек значением NULL
            insert_query = "INSERT INTO ESPTable ([Data], [Description], [Status], Sensor1, Sensor2, Sensor3, Sensor4, Sensor5, Sensor6, ESP_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (formatted_time, description, '404', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', '1')
            cursor.execute(insert_query, params)
            conn.commit()
            print('Вставка данных по умолчанию выполнена')
        except pyodbc.Error as ex:
            print("Ошибка при вставке данных по умолчанию таблицу ESPTable: ", ex)
        print(f'Контроллер {ip_address} недоступен, статус 404 записан в базу данных')
conn.close()
# Задержка в 5 секунд перед следующим запросом
time.sleep(2)

# Закрытие соединения с базой данных

print('Соединение с базой данных закрыто')
