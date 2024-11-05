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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm
from tg_users.models import TelegramUser
from tg_users.serializers import MemberSerializer


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
    form_class = EventForm
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmembers = event.participants.all()
    context = {"event": event, "eventmember": eventmembers}
    return render(request, "event-details.html", context)


class EventMemberView(APIView):
    def post(self, request, event_id):
        serializer = MemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data['telegram_id']
        event = get_object_or_404(Event, id=event_id)
        try:
            with transaction.atomic():
                telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                if event.participants.count() < event.max_participants:
                    if telegram_user not in event.participants.all():
                        event.participants.add(telegram_user)
                        return Response({"message": "Участник добавлен"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"error": "Этот пользователь уже добавлен к событию."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": "Достигнут максимум участников для этого события."}, status=status.HTTP_400_BAD_REQUEST)
        except TelegramUser.DoesNotExist:
            return Response({"error": "Пользователь с таким Telegram ID не найден."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Произошла ошибка при добавлении участника: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
