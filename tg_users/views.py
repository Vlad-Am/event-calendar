from django.contrib.auth.hashers import make_password

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


class CheckExistingUserView(viewsets.ViewSet):
    def list(self, request):
        serializer = MemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_id = serializer.validated_data['tg_id']
        telegram_user = TelegramUser.objects.filter(telegram_id=tg_id).first()
        return Response({'exists': bool(telegram_user)})


class CancelEventRegistrationView(viewsets.ViewSet):
    def create(self, request):
        try:
            serializer = EventMembersSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            event_id = serializer.validated_data['event_id']
            tg_id = serializer.validated_data['tg_id']
            print(event_id, tg_id)
            event = Event.objects.get(id=event_id)
            print(event)
            user = TelegramUser.objects.get(telegram_id=tg_id)
            print(user)
            if user in event.participants.all():
                event.participants.remove(user)
                return Response({"message": "Запись на тренировку успешно отменена"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Вы не записаны на эту тренировку"}, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({"error": "Мероприятие не найдено"}, status=status.HTTP_404_NOT_FOUND)
        except TelegramUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        except (KeyError, IndexError, ValueError):
            return Response({"error": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)


class GetUserEventsView(viewsets.ViewSet):
    def create(self, request):
        serializer = (MemberSerializer(data=request.data))
        serializer.is_valid(raise_exception=True)
        tg_id = serializer.validated_data['telegram_id']
        try:
            user = TelegramUser.objects.get(telegram_id=tg_id)
            events = Event.objects.filter(participants=user)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        except TelegramUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
