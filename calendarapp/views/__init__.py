from .event_list import AllEventsListView, CompletedEventsListView, RunningEventsListView, UpcomingEventsListView
from .other_views import (
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    EventMemberDeleteView,
    delete_event,
    next_week,
    next_day, EventMemberView, remove_member,
)


__all__ = [
    AllEventsListView,
    RunningEventsListView,
    UpcomingEventsListView,
    CompletedEventsListView,
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    remove_member,
    EventMemberView,
    EventMemberDeleteView,
    delete_event,
    next_week,
    next_day,
]
