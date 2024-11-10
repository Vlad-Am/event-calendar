from django.http import JsonResponse
from django.views.generic import ListView

from calendarapp.models import Event


class EventsListView(ListView):
    template_name = "calendarapp/events_list.html"
    model = Event
    paginate_by = 5
    ordering = ['-created_at']  # Сортируем по дате создания в обратном порядке

    def render_to_response(self, context, **response_kwargs):
        # Проверяем, что запрос требует JSON
        if self.request.headers.get('Accept') == 'application/json':
            events = list(self.get_queryset().values())  # Преобразуем QuerySet в список словарей
            return JsonResponse(events, safe=False)  # Возвращаем JSON ответ
        else:
            # Если не JSON, рендерим стандартный HTML-шаблон
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
    def paginate_queryset(self, queryset, page_size):
        # Переопределяем функцию пагинации для включения тренеров
        queryset = queryset.select_related('trainer')
        return super().paginate_queryset(queryset, page_size)


    def get_queryset(self):
        return Event.objects.get_upcoming_events(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = self.get_queryset()
        return context


class CompletedEventsListView(EventsListView):
    """ Completed events list view """

    def get_queryset(self):
        return Event.objects.get_completed_events(user=self.request.user)
