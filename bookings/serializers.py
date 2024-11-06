from rest_framework import serializers
from .models import Campsite, Booking

class CampsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campsite
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
