# Generated by Django 4.2.7 on 2024-10-25 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0006_event_max_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='max_participants',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]