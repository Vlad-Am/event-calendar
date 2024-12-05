from django.urls import path

from . import views
from .views.other_views import EventMemberView

app_name = "calendarapp"

urlpatterns = [
    path("calendar/", views.CalendarViewNew.as_view(), name="calendar"),
    path("calendars/", views.CalendarView.as_view(), name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path("event/<int:pk>/remove/", views.EventMemberDeleteView.as_view(), name="remove_event"),
    path("event/<int:event_id>/<int:member_id>/remove/", views.remove_member, name="remove_member"),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path("running-event-list/", views.RunningEventsListView.as_view(), name="running_events"),

    path("upcoming-event-list/", views.UpcomingEventsListView.as_view(), name="upcoming_events"),
    path("upcoming-event-list/<int:direction_id>/", views.UpcomingEventsListView.as_view(),
         name="upcoming_events_by_direction"),
    # path("upcoming-directions/", views.UpcomingDirectionsListView.as_view(), name="upcoming_directions"),

    path("completed-event-list/", views.CompletedEventsListView.as_view(), name="completed_events"),
    # Ручки для ТГ
    # path("add_eventmember/<int:event_id>/", views.add_eventmember, name="add_eventmember"),
    path("add_eventmember/<int:event_id>/", EventMemberView.as_view(), name="add_eventmember"),

]
