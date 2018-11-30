from django import forms

from .models import Schedule


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        exclude = ('author', 'recurrence', 'recur_until')
        widgets = {
            'date': forms.DateInput(attrs={"type": "date"}),
            'participants': forms.CheckboxSelectMultiple,
        }
