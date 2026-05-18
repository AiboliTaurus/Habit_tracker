from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с авторизацией по email"""

    email = models.EmailField(unique=True, db_index=True, verbose_name='Email')
    username = models.CharField(max_length=150, unique=True, verbose_name='Логин')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')

    # Telegram
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True,
                                        verbose_name='Telegram Chat ID')
    telegram_notifications = models.BooleanField(default=True,
                                                 verbose_name='Telegram уведомления')

    # Дополнительные поля
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    # Статусы
    is_staff = models.BooleanField(default=False, verbose_name='Staff status')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    last_activity = models.DateTimeField(default=timezone.now, verbose_name='Последняя активность')

    # Даты
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['telegram_chat_id']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def has_telegram(self):
        return bool(self.telegram_chat_id)


class Payment(models.Model):
    """Модель платежа"""

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        TRANSFER = 'transfer', 'Перевод на счет'
        CARD = 'card', 'Банковская карта'

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Ожидает оплаты'
        PAID = 'paid', 'Оплачен'
        FAILED = 'failed', 'Ошибка оплаты'
        REFUNDED = 'refunded', 'Возврат'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(
        max_length=10, choices=PaymentMethod.choices,
        default=PaymentMethod.TRANSFER, verbose_name='Способ оплаты'
    )
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING, verbose_name='Статус платежа'
    )

    class Meta:
        db_table = 'payments'
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Платеж {self.id}: {self.user.email} - {self.amount}₽"
