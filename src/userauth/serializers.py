from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


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

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError({"error": "Invalid username or password"})

        refresh = RefreshToken.for_user(user)
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refresh")
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise ValidationError({"error": "Invalid or expired refresh token"})
        return {"access_token": str(refresh.access_token)}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
        except TokenError:
            raise ValidationError({"error": "Invalid or expired refresh token"})
        token.blacklist()
        return {}
