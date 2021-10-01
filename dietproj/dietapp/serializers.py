from rest_framework import serializers
from dietapp.models import   Food, Event, Energy



class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields='__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model=Energy
        fields='__all__'

