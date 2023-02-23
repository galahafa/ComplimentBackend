from django.forms import ModelForm

from apps.models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

