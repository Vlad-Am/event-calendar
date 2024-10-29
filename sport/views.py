from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets

from .forms import TrainerForm, DirectionForm
from .models import Trainer, Direction
from .serializers import TrainerSerializer, DirectionSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'sport/trainer_list.html', {'trainers': trainers})


def trainer_create(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sport:trainer_list')
    else:
        form = TrainerForm()
    return render(request, 'sport/trainer_form.html', {'form': form})


def trainer_update(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        form = TrainerForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('sport:trainer_list')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'sport/trainer_form.html', {'form': form})


def trainer_delete(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    if request.method == 'POST':
        trainer.delete()
        return redirect('sport:trainer_list')
    return render(request, 'sport/trainer_confirm_delete.html', {'object': trainer})


def direction_list(request):
    directions = Direction.objects.all()
    return render(request, 'sport/direction_list.html', {'directions': directions})


def direction_create(request):
    if request.method == 'POST':
        form = DirectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sport:direction_list')
    else:
        form = DirectionForm()
    return render(request, 'sport/direction_form.html', {'form': form})


def direction_update(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        form = DirectionForm(request.POST, instance=direction)
        if form.is_valid():
            form.save()
            return redirect('sport:direction_list')
    else:
        form = DirectionForm(instance=direction)
    return render(request, 'sport/direction_form.html', {'form': form})


def direction_delete(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        direction.delete()
        return redirect('sport:direction_list')
    return render(request, 'sport/direction_confirm_delete.html', {'direction': direction})
