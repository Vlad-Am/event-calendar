from django.contrib import admin

from sport.models import Trainer, Direction


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    model = Trainer
    list_display = [
        "id",
        "qualification",
        "achievements",
        "name",

    ]
    search_fields = ["name"]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    model = Direction
    list_display = [
        "id",
        "name",
    ]

    search_fields = ["name"]
