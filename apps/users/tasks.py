from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def block_inactive_users():
    """
    Задача для блокировки неактивных пользователей.
    Блокирует пользователей, которые не заходили более месяца.
    """
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_blocked=False
    )

    count = inactive_users.update(is_blocked=True, is_active=False)

    return f"Blocked {count} inactive users"
