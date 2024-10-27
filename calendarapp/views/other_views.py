# cal/views.py
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm
from tg_users.models import TelegramUser


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        trainer = form.cleaned_data["trainer"]
        direction = form.cleaned_data["direction"]
        max_participants = form.cleaned_data["max_participants"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            trainer=trainer,
            direction=direction,
            max_participants=max_participants,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "trainer", "direction", "max_participants", "start_time", "end_time"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


@csrf_exempt
def add_eventmember(request, event_id):
    forms = AddMemberForm()
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            telegram_id = forms.cleaned_data["telegram_id"]

            try:
                with transaction.atomic():
                    # Получаем существующего пользователя TelegramUser или создаем нового
                    telegram_user, created = TelegramUser.objects.get_or_create(
                        telegram_id=telegram_id,
                    )

                    # Проверяем, не превышен ли лимит участников
                    if event.participants.count() < event.max_participants:
                        # Добавляем пользователя к событию
                        event.participants.add(telegram_user)
                        # Обновляем количество участников
                        event.save()
                        return redirect("calendarapp:event_details", event_id=event.id)
                    else:
                        forms.add_error(None, "Достигнут максимум участников для этого события.")
            except Exception as e:
                forms.add_error(None, f"Произошла ошибка при добавлении участника: {str(e)}")

    context = {"form": forms, "event": event}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_current = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {"id": event.id,
                 "title": event.title,
                 "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                 "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                 "description": event.description,
                 "trainer": f"{event.trainer}",
                 "direction": event.direction.id,
                 "max_participants": event.max_participants,
                 }
            )

        context = {"form": forms, "events": event_list,
                   "events_current": events_current}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return JsonResponse({'message': 'Event success delete.'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def next_week(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=7)
        next.end_time += timedelta(days=7)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def next_day(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        next = event
        next.id = None
        next.start_time += timedelta(days=1)
        next.end_time += timedelta(days=1)
        next.save()
        return JsonResponse({'message': 'Sucess!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)


def copy_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        new_event = Event(
            user=request.user,
            title=f'{event.title} (copy)',
            description=event.description,
            trainer=event.trainer,
            direction=event.direction,
            max_participants=event.max_participants,
            start_time=event.start_time + request["start_time"],
            end_time=event.end_time + request["end_time"],
        )
        new_event.save()
        return JsonResponse({'message': 'Success!'})
    else:
        return JsonResponse({'message': 'Error!'}, status=400)
