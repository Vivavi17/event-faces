from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email")
        extra_kwargs = {"password": {"write_only": True}}

    def is_valid(self, *args, **kwargs):
        if User.objects.filter(username=self.initial_data["username"]).exists():
            raise ValidationError("Username already exists")
        return super().is_valid(*args, **kwargs)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
