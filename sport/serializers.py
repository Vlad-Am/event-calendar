from rest_framework import serializers
from .models import Trainer, Direction


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class TrainerDirectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'name')


class TrainerSerializer(serializers.ModelSerializer):
    direction = TrainerDirectionsSerializer(many=True)

    class Meta:
        model = Trainer
        fields = '__all__'
