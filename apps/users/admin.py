from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Payment


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'telegram_chat_id', 'telegram_notifications', 'user_timezone', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'telegram_notifications', 'user_timezone', 'date_joined')
    search_fields = ('email', 'username', 'telegram_chat_id')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'city', 'avatar')}),
        ('Telegram', {'fields': ('telegram_chat_id', 'telegram_notifications')}),
        ('Timezone', {'fields': ('user_timezone',)}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_blocked', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'last_activity', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_date', 'amount', 'payment_method', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('payment_date',)
