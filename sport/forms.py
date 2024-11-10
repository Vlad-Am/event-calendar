from django import forms
from django.forms import ModelForm
from django_select2.forms import Select2MultipleWidget

from .models import Trainer, Direction


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

    def save(self, commit=True):
        trainer = super().save(commit=False)
        if commit:
            trainer.save()
            self.save_m2m()
        return trainer

    class Meta:
        model = Trainer
        fields = '__all__'


class TrainerWidget(Select2MultipleWidget):
    search_fields = [
        "name__icontains"
    ]


class DirectionForm(ModelForm):
    trainers = forms.ModelMultipleChoiceField(queryset=Trainer.objects.all(),
                                              widget=TrainerWidget, required=False)

    class Meta:
        model = Direction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DirectionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
        self.fields['name'].label = "Название"
        self.fields['trainers'].label = "Тренеры"
        # Код ниже по идее должен отвечать за выбор тренеров при редактировании, но не работает
        # пока форма без поиска по тренерам. Только мулитиселект выбор
        # TODO: Форма требует доработки для выбора тренеров
        # self.fields['trainers'].queryset = Trainer.objects.all()
        #
        # if self.instance.pk:
        #     self.fields['trainers'] = self.instance.trainers.all()

    # def save(self, commit=True):
    #     direction = super().save(commit=False)
    #     if commit:
    #         direction.save()
    #         self.save_m2m()
    #     return direction
