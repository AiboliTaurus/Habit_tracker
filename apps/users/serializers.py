from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор пользователя"""

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'telegram_chat_id', 'telegram_notifications', 'phone',
            'city', 'avatar', 'user_timezone', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 'user_timezone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TelegramChatIdSerializer(serializers.Serializer):
    """Сериализатор для установки Telegram Chat ID"""
    telegram_chat_id = serializers.CharField(max_length=100, required=True)


class SetTelegramNotificationsSerializer(serializers.Serializer):
    """Сериализатор для настройки Telegram уведомлений"""
    enabled = serializers.BooleanField(required=True)


class SetTimezoneSerializer(serializers.Serializer):
    """Сериализатор для установки часового пояса"""
    user_timezone = serializers.CharField(max_length=50, required=True)


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_email', 'payment_date', 'amount',
                  'payment_method', 'status']
        read_only_fields = ['id', 'payment_date', 'status']
