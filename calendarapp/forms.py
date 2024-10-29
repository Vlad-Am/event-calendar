from django.forms import ModelForm, DateInput
from calendarapp.models import Event
from django import forms
from django_select2 import forms as s2forms


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
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название мероприятия"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control",
                       "placeholder": "Введите описание мероприятия",
                       }
            ),
            "start_time": DateInput(

                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "max_participants": forms.NumberInput(
                attrs={"class": "form-control",
                       "placeholder": "Введите максимальное количество участников(опционально)"}
            ),
            "trainer": forms.Select(attrs={"class": "form-control"}),
            "direction": forms.Select(attrs={"class": "form-control"}),
            "participants": ParticipantsWidget(attrs={"class": "form-control"}),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class AddMemberForm(forms.Form):
    telegram_id = forms.CharField(max_length=100, label="Telegram ID")
