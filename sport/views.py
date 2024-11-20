from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, ListView
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


class TrainerListView(ListView):
    model = Trainer
    template_name = 'sport/trainer_list.html'
    context_object_name = 'trainers'


class TrainerCreateView(CreateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'sport/trainer_form.html'
    success_url = reverse_lazy('sport:trainer_list')


class TrainerUpdateView(UpdateView):
    model = Trainer
    form_class = TrainerForm
    template_name = 'sport/trainer_form.html'
    success_url = reverse_lazy('sport:trainer_list')


class TrainerDeleteView(DeleteView):
    model = Trainer
    template_name = 'sport/trainer_confirm_delete.html'
    success_url = reverse_lazy('sport:trainer_list')


class DirectionListView(ListView):
    model = Direction
    template_name = 'sport/direction_list.html'
    context_object_name = 'directions'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Создаем словарь направлений и их тренеров
        direction_trainers = {}
        for direction in context['directions']:
            direction_trainers[direction] = direction.trainer_directions.all()
        print(direction_trainers)
        # Добавляем словарь в контекст
        context['direction_trainers'] = direction_trainers
        return context


class DirectionCreateView(CreateView):
    model = Direction
    form_class = DirectionForm
    template_name = 'sport/direction_form.html'
    success_url = reverse_lazy('sport:direction_list')


class DirectionUpdateView(UpdateView):
    model = Direction
    form_class = DirectionForm
    template_name = 'sport/direction_form.html'
    success_url = reverse_lazy('sport:direction_list')


class DirectionDeleteView(DeleteView):
    model = Direction
    template_name = 'sport/direction_confirm_delete.html'
    success_url = reverse_lazy('sport:direction_list')