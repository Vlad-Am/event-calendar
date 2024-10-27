from django.urls import path

from .apps import TgUsersConfig
from .views import CreateTelegramUser

app_name = TgUsersConfig.name

urlpatterns = [
    path('create/', CreateTelegramUser.as_view(), name='create_telegram_user'),
]
