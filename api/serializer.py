from rest_framework import serializers

class Weather_serializer(serializers.Serializer):
    city= serializers.CharField(max_length=100)
    temperature= serializers.FloatField()
    description= serializers.CharField(max_length=255)