from django.db import models
from django.db.models import ForeignKey

from accounts.models import User


class TelegramUser(models.Model):
    full_name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=100, unique=True)
    is_subscribed = models.BooleanField(default=False)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "Телеграм-пользователь"
        verbose_name_plural = "Телеграм-пользователи"


