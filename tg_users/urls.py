from django.urls import path
from rest_framework import routers

from .apps import TgUsersConfig
from .views import CreateTelegramUser, CheckExistingUserView, CancelEventRegistrationView, GetUserEventsView

app_name = TgUsersConfig.name

router = routers.DefaultRouter()
router.register(r'check_existing_user', CheckExistingUserView, basename='check_existing_user')
router.register(r'cancel_registration', CancelEventRegistrationView, basename='cancel_registration')
router.register(r'user_events', GetUserEventsView, basename='user_events')

urlpatterns = [
                  path('create/', CreateTelegramUser.as_view(), name='create_telegram_user'),
              ] + router.urls
