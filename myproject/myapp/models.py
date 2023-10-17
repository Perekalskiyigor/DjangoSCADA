from django.db import models

class SensorData(models.Model):
    sensor1 = models.FloatField()
    sensor2 = models.FloatField()
    sensor3 = models.FloatField()
    sensor4 = models.FloatField()