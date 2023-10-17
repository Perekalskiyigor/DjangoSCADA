from django.shortcuts import render
from .models import SensorData

def sensor_data(request):
    data = SensorData.objects.all()
    return render(request, 'sensor_data.html', {'data': data})
