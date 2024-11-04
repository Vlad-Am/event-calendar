from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from calendarapp.models import Event
from .models import TelegramUser
from .serializers import TelegramUserSerializer, EventSerializer


class CreateTelegramUser(APIView):
    """
    Create a new Telegram user.
    """

    def post(self, request):
        telegram_id = request.data.get('telegram_id')

        # Проверяем, существует ли пользователь с таким telegram_id
        telegram_user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
        if telegram_user:
            return Response({'error': 'Пользователь с таким telegram_id уже существует.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем нового пользователя с базовым паролем
        user = User(
            email=f"{telegram_id}@telegram.ru",
            password=make_password("base"),
            telegram_id=telegram_id,
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


@csrf_exempt
@api_view(['GET'])
def check_existing_user_by_tg(request, tg_id):
    """
    Check if Telegram user with given telegram_id already exists.
    """
    telegram_user = TelegramUser.objects.filter(telegram_id=tg_id).first()
    if telegram_user:
        return Response({'exists': True}, status=status.HTTP_200_OK)
    else:
        return Response({'exists': False}, status=status.HTTP_200_OK)


@api_view(['POST'])
def cancel_event_registration(request, event_id, tg_id):
    try:
        event = Event.objects.get(id=event_id)
        user = User.objects.get(telegram_id=tg_id)
        if user in event.participants.all():
            event.participants.remove(user)
            return Response({"message": "Запись на тренировку успешно отменена"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Вы не записаны на эту тренировку"}, status=status.HTTP_400_BAD_REQUEST)
    except Event.DoesNotExist:
        return Response({"error": "Мероприятие не найдено"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_events(request, tg_id):
    user = User.objects.get(telegram_id=tg_id)
    events = Event.objects.filter(participants=user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
