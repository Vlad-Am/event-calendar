from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from calendarapp.models import Event
from .models import TelegramUser
from .serializers import TelegramUserSerializer, EventSerializer, EventMembersSerializer, MemberSerializer


class CreateTelegramUser(APIView):
    """
    Create a new Telegram user.
    """

    def post(self, request):
        tg_id = request.data.get('tg_id')

        # Проверяем, существует ли пользователь с таким telegram id
        telegram_user = TelegramUser.objects.filter(tg_id=tg_id).first()
        if telegram_user:
            return Response({'error': 'Пользователь с таким telegram id уже существует.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем нового пользователя с базовым паролем
        user = User(
            email=f"{tg_id}@telegram.ru",
            password=make_password("base"),
            tg_id=tg_id,
            is_active=True
        )
        user.save()

        # Создаем TelegramUser и связываем с новым User
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Связываем нового пользователя с TelegramUser
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = TelegramUser.objects.get(pk=pk)
        serializer = TelegramUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = TelegramUser.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckExistingUserView(APIView):
    def get(self, request, tg_id):
        telegram_user = TelegramUser.objects.filter(tg_id=tg_id).first()
        return Response({'exists': bool(telegram_user)})


class CancelEventRegistrationView(APIView):
    def post(self, request):
        serializer = EventMembersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Извлекаем данные из сериализатора
        event_id = serializer.validated_data['event_id']
        tg_id = serializer.validated_data['tg_id']

        # Получаем Event и TelegramUser или возвращаем 404
        event = get_object_or_404(Event, id=event_id)
        user = get_object_or_404(TelegramUser, tg_id=tg_id)

        # Проверяем, что пользователь зарегистрирован на событие
        if user in event.participants.all():
            event.participants.remove(user)
            return Response({"message": "Запись на тренировку успешно отменена"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Вы не записаны на эту тренировку"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllUserEventsView(APIView):
    def get(self, request, tg_id):
        # Получаем пользователя с tg_id или возвращаем 404
        user = get_object_or_404(TelegramUser, tg_id=tg_id)

        # Фильтруем события по участнику
        events = Event.objects.filter(participants=user).annotate(participants_count=Count('participants'))

        # Сериализация и возврат данных
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class GetUpcomingUserEventsView(APIView):
    def get(self, request, tg_id):
        # Получаем пользователя с tg_id или возвращаем 404
        user = get_object_or_404(TelegramUser, tg_id=tg_id)

        participant_counts = (Event.objects.filter(pk=OuterRef('pk'))
                              .annotate(count=Count('participants')).values('count'))
        events = (Event.objects.filter(participants=user, start_time__gt=datetime.now())
                  .annotate(participants_count=Subquery(participant_counts)))

        # Сериализация и возврат данных
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class GetCompletedUserEventsView(APIView):
    def get(self, request, tg_id):
        # Получаем пользователя с tg_id или возвращаем 404
        user = get_object_or_404(TelegramUser, tg_id=tg_id)

        # Фильтруем события по участнику и времени
        events = (Event.objects.filter(participants=user, start_time__lt=datetime.now())
                  .annotate(participants_count=Count('participants')))

        # Сериализация и возврат данных
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


# class GetAvailableDirectionsForUserView(APIView):
#
#     def get(self, request, tg_id):
#         ...


class GetAvailableEventsForUserView(APIView):

    def get(self, request, tg_id):
        user = get_object_or_404(TelegramUser, tg_id=tg_id)

        # Фильтруем события по участнику и времени
        events = (
            Event.objects
            .exclude(participants=user)
            .filter(start_time__gt=datetime.now())
            .annotate(participants_count=Count('participants'))
            .order_by("start_time")
        )

        # Сериализация и возврат данных
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
