# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView as LoginOldView
from django.shortcuts import redirect

from django.urls import reverse
from django.views import View, generic
from django.views.generic import TemplateView

from apps.models import User
from apps.v1_0.forms.users import RegistrationForm, AuthenticationForm


class LoginView(LoginOldView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('main')


class StartPageView(TemplateView):
    template_name = 'start_page.html'


class RegistrationView(generic.CreateView):
    template_name = 'registration.html'
    model = User
    form_class = RegistrationForm

    def get_success_url(self):
        return reverse('main')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
            else:
                pass
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# class PasswordRecovery1