from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TelegramUser
from .serializers import TelegramUserSerializer


class CreateTelegramUser(APIView):
    """
    Create a new Telegram user.
    """
    def post(self, request):
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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