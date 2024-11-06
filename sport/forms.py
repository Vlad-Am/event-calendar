from django import forms
from django.forms import ModelForm
from django_select2.forms import Select2MultipleWidget

from .models import Trainer, Direction
from django_select2 import forms as s2forms


class TrainerForm(forms.ModelForm):
    qualification = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control auto-expand'}))
    achievements = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control auto-expand'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

        self.fields['name'].label = "ФИО"
        self.fields['qualification'].label = "Квалификация"
        self.fields['achievements'].label = "Достижения"
        self.fields['direction'].label = "Направление"

    class Meta:
        model = Trainer
        fields = '__all__'


class TrainerWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
        "qualification__icontains",
        "achievements__icontains",
    ]

class DirectionForm(ModelForm):
    class Meta:
        model = Direction
        fields = '__all__'
        widgets = {
            'trainers': TrainerWidget(attrs={'data-placeholder': 'Выберите тренеров...'}),
        }

    def __init__(self, *args, **kwargs):
        super(DirectionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields['name'].label = "Название"
        self.fields['trainers'].label = "Тренеры"

        if self.instance.pk:
            self.fields['trainers'].queryset = self.instance.trainers.all()

    def save(self, commit=True):
        direction = super().save(commit=False)
        if commit:
            direction.save()
            self.save_m2m()
        return direction
