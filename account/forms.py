from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'last_name', 'first_name', 'email')
