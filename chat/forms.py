from django import forms

from .models import Message


class MessageForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "メッセージを入力", 'rows': 5}), label="")

    class Meta:
        model = Message
        fields = ('content',)
