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
        if self.instance.pk:  # Если это обновление, заполняем поле directions
            self.fields['direction'].initial = self.instance.direction.all()
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
        widgets = {
            'direction': Select2MultipleWidget,
        }

    # def save(self, commit=True):
    #     trainer = super().save(commit=False)
    #     if commit:
    #         trainer.save()
    #         # Удаляем все старые связи
    #         trainer.directions.clear()
    #         # Добавляем новые связи
    #         trainer.direction.set(self.cleaned_data['direction'])
    #         trainer.save()
    #     return trainer


class TrainerWidget(Select2MultipleWidget):
    search_fields = [
        "name__icontains",
        "qualification__icontains",
        "achievements__icontains",
    ]


class DirectionForm(forms.ModelForm):
    trainer_directions = forms.ModelMultipleChoiceField(
        queryset=Trainer.objects.all(),
        widget=TrainerWidget,
        required=False,
        label="Тренеры"
    )

    class Meta:
        model = Direction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DirectionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields['name'].label = "Название"
        self.fields['trainer_directions'].label = "Тренеры"

        if self.instance.pk:
            self.fields['trainer_directions'].initial = self.instance.trainer_directions.all()

    def save(self, commit=True):
        instance = super(DirectionForm, self).save(commit=False)
        if commit:
            instance.save()
            instance.trainer_directions.set(self.cleaned_data['trainer_directions'])
            instance.save()
        return instance
