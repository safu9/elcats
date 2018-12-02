from django import forms

from .models import Schedule, ScheduleComment


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        exclude = ('author', 'recurrence', 'recur_until')
        widgets = {
            'date': forms.DateInput(attrs={"type": "date"}),
            'participants': forms.CheckboxSelectMultiple,
        }


class ScheduleCommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "コメントを入力", 'rows': 5}), label="")

    class Meta:
        model = ScheduleComment
        fields = ('content',)
