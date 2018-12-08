from django import forms

from home.models import Project
from .models import Page


class PageForm(forms.ModelForm):

    project = forms.ModelChoiceField(Project.objects.all(), widget=forms.HiddenInput, disabled=True)

    class Meta:
        model = Page
        fields = ('project', 'name', 'slug', 'content')
        help_texts = {
            'slug': 'URLなどに使われ、半角の英数字、アンダースコア、ハイフンのみ使用できます。',
        }
