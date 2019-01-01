from django import forms
from django.db.models import Q

from .models import Task, TaskComment


class TaskSearchForm(forms.Form):
    keyword = forms.CharField(label='', max_length=500, required=False)
    state = forms.CharField(label='', max_length=20, required=False, widget=forms.HiddenInput)

    def filter_query(self, query):
        if not self.is_valid():
            return query

        state = self.cleaned_data['state']
        if state == 'done':
            query = query.filter(state=2)
        else:
            query = query.exclude(state=2)

        keyword = self.cleaned_data['keyword'].strip()
        if keyword:
            for w in keyword.split():
                query = query.filter(Q(name__contains=w) | Q(description__contains=w))

        return query


class TaskForm(forms.ModelForm):

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            self.fields['assignees'].queryset = project.members.all()

    class Meta:
        model = Task
        exclude = ('project', 'number', 'author',)
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
