from django import forms
from .models import Trainer, Direction


class TrainerForm(forms.ModelForm):
    qualification = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control auto-expand'}))
    achievements = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control auto-expand'}),
                                   required=False)

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


class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['name'].label = "Название"
        self.fields['description'].label = "Описание"
