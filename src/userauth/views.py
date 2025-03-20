from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RefreshSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response(
            {
                "message": "User created successfully",
                "refresh_token": str(refresh),
                "access_token": str(access),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            raise ValidationError({"error": "Invalid username or password"})
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response(
            {
                "refresh_token": str(refresh),
                "access_token": str(access),
            },
            status=status.HTTP_200_OK,
        )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            raise ValidationError({"error": "Invalid or expired refresh token"})
        return Response(
            {"access_token": str(refresh.access_token)}, status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh"]
        try:
            token = RefreshToken(refresh_token)
        except TokenError:
            raise ValidationError({"error": "Invalid or expired refresh token"})
        token.blacklist()
        return Response({}, status=status.HTTP_200_OK)
