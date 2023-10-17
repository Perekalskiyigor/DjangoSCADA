import requests
import time
import json
from .models import SensorData

def fetch_data():
    while True:
        response = requests.get('http://208.55.66.77')
        data = response.json()
        SensorData.objects.create(sensor1=data['SEnsor1'], sensor2=data['SEnsor2'], sensor3=data['SEnsor3'], sensor4=data['SEnsor4'])
        time.sleep(5)