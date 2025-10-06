from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import (LoginSerializer, RegisterSerializer,
                               TokenRefreshSerializer, TokenSerializer)

from .services import AuthUtil


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = self.get_serializer(instance=user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token_pair = AuthUtil.generate_token_pair(user)
        token_serializer = TokenSerializer(token_pair)
        return Response(
            {"message": "Login success", **token_serializer.data},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="token/refresh")
    def refresh_token(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"access": serializer.validated_data["access"]},
            status=status.HTTP_200_OK,
        )
