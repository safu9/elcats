from django import forms

from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('author',)
        widgets = {
            'date_from': forms.DateInput(attrs={"type": "date"}),
            'date_to': forms.DateInput(attrs={"type": "date"}),
            'assignees': forms.CheckboxSelectMultiple,
        }
