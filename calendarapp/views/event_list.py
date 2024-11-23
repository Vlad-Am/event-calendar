from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView

from calendarapp.models import Event
from tg_users.serializers import EventSerializer


class EventsListView(ListView):
    template_name = "calendarapp/events_list.html"
    model = Event

    def render_to_response(self, context, **response_kwargs):
        # Проверяем, что запрос требует JSON
        if self.request.headers.get('Accept') == 'application/json':
            # events = list(self.get_queryset().values())  # Преобразуем QuerySet в список словарей
            # return JsonResponse(events, safe=False)  # Возвращаем JSON ответ
            events = self.get_queryset()
            serializer = EventSerializer(events, many=True)
            return JsonResponse(serializer.data, safe=False)  # Возвращаем JSON ответ

        return super().render_to_response(context, **response_kwargs)


class AllEventsListView(EventsListView):
    """ All event list views """

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)


class RunningEventsListView(EventsListView):
    """ Running events list view """

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)


class UpcomingEventsListView(EventsListView):
    """ Upcoming events list view """

    template_name = "calendarapp/upcoming_events_list.html"

    def get_queryset(self):
        direction_id = self.kwargs.get('direction_id')
        if direction_id:
            return Event.objects.get_upcoming_events(user=self.request.user).filter(direction_id=direction_id)
        return Event.objects.get_upcoming_events(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = self.get_queryset()
        return context


class CompletedEventsListView(EventsListView):
    """ Completed events list view """

    def get_queryset(self):
        return Event.objects.get_completed_events(user=self.request.user)


# class UpcomingDirectionsListView(View):
#     """ View для получения направлений с предстоящими событиями """
#
#     def get(self, request, *args, **kwargs):
#         # Используем метод менеджера для получения направлений
#         directions = Event.objects.get_directions_for_upcoming_events(user=request.user)
#
#         # Преобразуем QuerySet в список словарей с необходимыми полями (например, id и name)
#         directions_data = [{'id': direction.id, 'name': direction.name} for direction in directions]
#
#         return JsonResponse(directions_data, safe=False)
