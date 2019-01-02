from django import forms
from django.db.models import Q

from .models import Schedule, ScheduleComment


class ScheduleSearchForm(forms.Form):
    keyword = forms.CharField(label='', max_length=500, required=False)
    type = forms.CharField(label='', max_length=20, required=False, widget=forms.HiddenInput)

    def filter_query(self, query, user):
        if not self.is_valid():
            return query

        type = self.cleaned_data['type']
        if type != 'all':
            query = query.filter(participants=user)

        keyword = self.cleaned_data['keyword'].strip()
        if keyword:
            for w in keyword.split():
                query = query.filter(Q(name__contains=w) | Q(description__contains=w))

        return query


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
