from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    SetTelegramChatIdView, SetTelegramNotificationsView,
    SetTimezoneView, CurrentUserView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('current/', CurrentUserView.as_view(), name='current_user'),
    path('set-telegram-id/', SetTelegramChatIdView.as_view(), name='set-telegram-id'),
    path('set-telegram-notifications/', SetTelegramNotificationsView.as_view(), name='set-telegram-notifications'),
    path('set-timezone/', SetTimezoneView.as_view(), name='set-timezone'),
]
