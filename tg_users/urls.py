from django.urls import path

from .apps import TgUsersConfig
from .views import (CreateTelegramUser, CheckExistingUserView, CancelEventRegistrationView,
                    GetAllUserEventsView, GetUpcomingUserEventsView, GetCompletedUserEventsView,
                    GetAvailableEventsForUserView)

app_name = TgUsersConfig.name


urlpatterns = [
    path('create/', CreateTelegramUser.as_view(), name='create_telegram_user'),
    path('check_existing_user/<str:tg_id>', CheckExistingUserView.as_view(), name='check_existing_user'),
    path('cancel_registration', CancelEventRegistrationView.as_view(), name='cancel_registration'),

    path('all_user_events/<str:tg_id>', GetAllUserEventsView.as_view(), name='user_events_all'),
    path('upcoming_user_events/<str:tg_id>', GetUpcomingUserEventsView.as_view(), name='user_events_upcoming'),
    path('completed_user_events/<str:tg_id>', GetCompletedUserEventsView.as_view(), name='user_events_completed'),

    # path('available_directions/<str:tg_id>', GetAvailableDirectionsForUserView.as_view(), name='available_directions'),
    path('available_events/<str:tg_id>', GetAvailableEventsForUserView.as_view(), name='available_events')
]
