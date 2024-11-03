# Generated by Django 4.2.7 on 2024-10-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('telegram_id', models.CharField(max_length=100, unique=True)),
                ('is_subscribed', models.BooleanField(default=False)),
            ],
        ),
    ]