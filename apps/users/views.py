from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserSerializer, RegisterSerializer,
    TelegramChatIdSerializer, SetTelegramNotificationsSerializer,
    SetTimezoneSerializer
)


class RegisterView(generics.CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        responses={201: UserSerializer()}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Пользователь успешно зарегистрирован',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Профиль пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class SetTelegramChatIdView(generics.UpdateAPIView):
    """Установка Telegram Chat ID"""
    serializer_class = TelegramChatIdSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.telegram_chat_id = serializer.validated_data['telegram_chat_id']
        user.save()
        return Response({
            'message': 'Telegram Chat ID успешно установлен',
            'telegram_chat_id': user.telegram_chat_id
        })


class SetTelegramNotificationsView(generics.UpdateAPIView):
    """Настройка Telegram уведомлений"""
    serializer_class = SetTelegramNotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.telegram_notifications = serializer.validated_data['enabled']
        user.save()
        return Response({
            'message': f'Telegram уведомления {"включены" if user.telegram_notifications else "выключены"}',
            'telegram_notifications': user.telegram_notifications
        })


class SetTimezoneView(generics.UpdateAPIView):
    """Установка часового пояса пользователя"""
    serializer_class = SetTimezoneSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.user_timezone = serializer.validated_data['user_timezone']
        user.save()
        return Response({
            'message': f'Часовой пояс установлен: {user.user_timezone}',
            'user_timezone': user.user_timezone
        })


class CurrentUserView(generics.RetrieveAPIView):
    """Получение информации о текущем пользователе"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
