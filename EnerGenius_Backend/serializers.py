from rest_framework import serializers
from core.models import User, EnergyConsumption

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "phone_number", "profile_picture"]
    
class EnergyConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyConsumption
        fields = '__all__'
