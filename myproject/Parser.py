import pyodbc
import requests
import json
import time



# Подключение к базе данных MS SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=10.11.21.24;'
                      'Database=BI_TEST;'
                      'UID=Perekalskiy_igor;'
                      'PWD=Fnkfynblf198714;')
print('Подключение к базе данных')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Запрос к базе данных для получения всех IP-адресов из таблицы ESP_IP
cursor.execute("SELECT ip_address, Description, NameSensor FROM ESP_IP")

# Получение всех IP-адресов
for row in cursor.fetchall():
    ip_address = row.ip_address
    description = row.Description
    # Выполнение HTTP-запроса к устройству
    response = requests.get(f'http://{ip_address}/sensor_data')

    # Проверка статуса ответа
    if response.status_code == 200:
        # Получение данных сенсоров из ответа
        sensor_data = response.json()
        # Запись данных сенсоров в базу данных
        cursor.execute("{CALL [BI_TEST].[dbo].[ESPReceiver] (?, ?, ?, ?, ?, ?, ?, ?)}", sensor_data['Description'], '200', sensor_data['Sensor1'], sensor_data['Sensor2'], sensor_data['Sensor3'], sensor_data['Sensor4'], sensor_data['Sensor5'], sensor_data['Sensor6'])
        print('Данные сенсоров записаны в базу данных')
    else:
        # Запись статуса 404 и заполнение всех ячеек значением NULL
        cursor.execute("{CALL [BI_TEST].[dbo].[ESPReceiver] (?, ?, ?, ?, ?, ?, ?, ?)}", sensor_data['Description'], '404', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')
        print('Контроллер недоступен, статус 404 записан в базу данных')
    # Задержка в 5 секунд перед следующим запросом
    time.sleep(5)

# Закрытие соединения с базой данных
conn.close()
print('Соединение с базой данных закрыто')
