from django.db import models
from django.db.models import ForeignKey

from accounts.models import User


class TelegramUser(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
    birth_date = models.DateField(verbose_name='Дата рождения')

    tg_id = models.CharField(max_length=100, unique=True, verbose_name='Telegram ID')
    tg_full_name = models.CharField(max_length=255, verbose_name='Telegram Full Name')
    tg_username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Telegram Username')
    is_subscribed = models.BooleanField(default=False)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.phone_number})"

    class Meta:
        verbose_name = "Телеграм-пользователь"
        verbose_name_plural = "Телеграм-пользователи"


