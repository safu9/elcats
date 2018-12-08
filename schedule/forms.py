from django import forms

from .models import Schedule, ScheduleComment


class ScheduleForm(forms.ModelForm):

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            self.fields['participants'].queryset = project.members.all()

    class Meta:
        model = Schedule
        exclude = ('project', 'author', 'recurrence', 'recur_until')
        widgets = {
            'date': forms.DateInput(attrs={"type": "date"}),
            'participants': forms.CheckboxSelectMultiple,
        }


class ScheduleCommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "コメントを入力", 'rows': 5}), label="")

    class Meta:
        model = ScheduleComment
        fields = ('content',)
