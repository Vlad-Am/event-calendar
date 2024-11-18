from django.contrib import admin

from sport.models import Trainer, Direction


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    model = Trainer
    list_display = [
        "id",
        "name",
        "get_directions",
        "qualification",
        "achievements"
    ]
    search_fields = ["name"]

    def get_directions(self, obj):
        return ", ".join([direction.name for direction in obj.direction.all()])

    get_directions.short_description = 'Directions'


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    model = Direction
    list_display = [
        "id",
        "name",
        "get_trainers"
    ]

    search_fields = ["name"]

    def get_trainers(self, obj):
        return ", ".join([trainer.name for trainer in obj.trainers.all()])

    get_trainers.short_description = 'Trainers'
