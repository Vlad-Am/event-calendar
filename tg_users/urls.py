from django.urls import path

from .apps import TgUsersConfig
from .views import CreateTelegramUser, check_existing_user_by_tg, cancel_event_registration, get_user_events

app_name = TgUsersConfig.name

urlpatterns = [
    path('create/', CreateTelegramUser.as_view(), name='create_telegram_user'),
    path('check_existing_user/<str:tg_id>/', check_existing_user_by_tg, name="check_existing"),
    path('cancel_registration/<int:event_id>/<str:tg_id>/',
         cancel_event_registration, name="cancel_registration"),
    path('user_events/<str:tg_id>/', get_user_events, name="user_events"),

]
