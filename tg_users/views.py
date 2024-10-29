from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .models import TelegramUser
from .serializers import TelegramUserSerializer


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