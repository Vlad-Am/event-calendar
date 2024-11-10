import json

from django.contrib.postgres.search import SearchVector
from django.forms import ModelForm, DateInput
from calendarapp.models import Event
from django import forms
from django_select2 import forms as s2forms

from tg_users.models import TelegramUser


class ParticipantsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "telegram_id__icontains",
        "full_name__icontains",
    ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time",
                  "trainer", "max_participants", "direction", "participants"]
        labels = {
            "trainer": "Тренер",
            "participants": "Участники",
            "max_participants": "Максимальное количество участников",
            "direction": "Направление",
            "title": "Название",
            "description": "Описание",
            "start_time": "Начало",
            "end_time": "Окончание",
        }
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Введите название мероприятия"}
            ),
            "description": forms.Textarea(
                attrs={"rows": "3", "placeholder": "Введите описание мероприятия"}
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "max_participants": forms.NumberInput(
                attrs={"placeholder": "Введите максимальное количество участников(опционально)"}
            ),
            "trainer": forms.Select(),
            "direction": forms.Select(),
            "participants": ParticipantsWidget(
                attrs={"placeholder": "Выберите участников"}),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        for field in self.fields:
            if field == "start_time" or field == "end_time":
                self.fields[field].input_formats = ("%Y-%m-%dT%H:%M",)
                #  add form-control in widget
            self.fields[field].widget.attrs["class"] = "form-control"


class AddMemberForm(forms.Form):
    telegram_id = forms.IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        try:
            # Попытка обработки JSON, если данные пришли в формате JSON
            data = json.loads(self.data.get('telegram_id', '{}'))
            cleaned_data['telegram_id'] = data.get('telegram_id')
        except json.JSONDecodeError:
            pass  # Обработка как обычная форма
        return cleaned_data
