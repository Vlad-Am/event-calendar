# Generated by Django 4.2.7 on 2024-11-04 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0004_trainer_photo_alter_trainer_direction'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='description',
            field=models.TextField(default='', verbose_name='Описание'),
        ),
    ]
