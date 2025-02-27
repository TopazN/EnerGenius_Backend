from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)  # וודאי שתומך בקבצים

    class Meta:
        model = User
        fields = ["id", "email", "password", "full_name", "phone_number", "profile_picture"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
      password = validated_data.pop("password", None)
      user = User.objects.create_user(**validated_data)
      if password:
        user.set_password(password)
        user.save()
        return user