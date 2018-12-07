from django import forms

from .models import Task, TaskComment


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('project', 'author',)
        widgets = {
            'scheduled_date_from': forms.DateInput(attrs={"type": "date"}),
            'scheduled_date_to': forms.DateInput(attrs={"type": "date"}),
            'date_from': forms.DateInput(attrs={"type": "date"}),
            'date_to': forms.DateInput(attrs={"type": "date"}),
            'assignees': forms.CheckboxSelectMultiple,
        }


class TaskCommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "コメントを入力", 'rows': 5}), label="")

    class Meta:
        model = TaskComment
        fields = ('content',)
