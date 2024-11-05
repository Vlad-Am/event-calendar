from rest_framework import serializers

from calendarapp.models import Event
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['full_name', 'telegram_id', 'is_subscribed']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'participants', 'start_time', 'end_time', 'trainer', 'direction']


class AddMemberSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()


class CheckExistingUserSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()


class CancelEventRegistrationSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
    event_id = serializers.IntegerField()


class GetUserEventsSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()
