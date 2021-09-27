from rest_framework import serializers
from webapi.models import InputData, Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [ 'id', 'token' ]

class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputData
        fields = [ 'id', 'datetime', 'heartRate', 'steps', 'temperature' ]
