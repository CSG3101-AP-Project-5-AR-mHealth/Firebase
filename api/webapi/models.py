from django.db import models

class Registration(models.Model):
    token = models.CharField(max_length=162)

class InputData(models.Model):
    datetime = models.DateTimeField()
    heartRate = models.IntegerField()
    steps = models.IntegerField()
