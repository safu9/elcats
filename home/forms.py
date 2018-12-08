from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'slug', 'description', 'members', 'is_private')
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }
        help_texts = {
            'slug': 'URLなどに使われ、半角の英数字、アンダースコア、ハイフンのみ使用できます。',
            'is_private': 'このプロジェクトの内容をメンバー以外に非公開にします。',
        }
