from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)  # וודאי שתומך בקבצים

    class Meta:
        model = User
        fields = ["id", "email", "password", "full_name", "phone_number", "profile_picture"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            profile_picture=validated_data.get("profile_picture", None)
        )
        return user