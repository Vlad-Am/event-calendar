from datetime import datetime

from rest_framework import serializers

from calendarapp.models import Event
from sport.serializers import TrainerSerializer, DirectionSerializer
from .models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    birth_date = serializers.CharField()

    class Meta:
        model = TelegramUser
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'birth_date',
            'tg_id',
            'tg_full_name',
            'tg_username',
            'is_subscribed',
            'user'
        ]
        read_only_fields = ['user']

    def validate_birth_date(self, value):
        try:
            # Парсим дату из формата ДД.ММ.ГГГГ
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            # Возвращаем дату в формате, который ожидает Django
            return parsed_date.date()
        except ValueError:
            raise serializers.ValidationError("Неверный формат даты. Используйте ДД.ММ.ГГГГ.")


class EventSerializer(serializers.ModelSerializer):
    trainer = TrainerSerializer()
    direction = DirectionSerializer()
    participants_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'participants', 'start_time', 'end_time', 'trainer', 'direction',
                  'max_participants', 'participants_count']


class MemberSerializer(serializers.Serializer):
    tg_id = serializers.CharField()


class EventMembersSerializer(MemberSerializer):
    event_id = serializers.IntegerField()
    tg_id = serializers.CharField()



