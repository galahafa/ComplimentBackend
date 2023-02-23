from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as LoginOldView
from django.urls import reverse


class LoginView(LoginOldView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('main')

