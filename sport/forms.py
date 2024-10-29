from django import forms
from .models import Trainer, Direction


class TrainerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['name'].label = "ФИО"
        self.fields['qualification'].label = "Квалификация"
        self.fields['achievements'].label = "Достижения"
        self.fields['direction'].label = "Направление"
        self.fields['direction'].empty_label = "Выберите направление"

    class Meta:
        model = Trainer
        fields = '__all__'


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['name'].label = "Название"
