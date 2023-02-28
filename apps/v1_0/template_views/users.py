# from django.contrib.auth.forms import AuthenticationForm
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.views import LoginView as LoginOldView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url

from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic import TemplateView, RedirectView

from apps.common_utils.functions import get_random_integer
from apps.models import User
from apps.models.users import UserRecovery
from apps.v1_0.forms.users import RegistrationForm, AuthenticationForm, ForgotEmailForm, RecoveryForm


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


class ForgotEmailView(generic.CreateView):
    template_name = 'forgot_email.html'
    model = User
    form_class = ForgotEmailForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.data.get('email'))
            code = get_random_integer(6)
            print(code)
            store_code = make_password(code)
            user_recovery, _ = UserRecovery.objects.get_or_create(user=user)
            user_recovery.code = store_code
            user_recovery.save()
            subject = 'Password recovery'
            message = f'It is okay sometimes forget password, ' \
                      f'take this code: {code} ' \
                      f'enter and enjoy your day'
            email_from = settings.EMAIL_HOST_USER

            recipient_list = [form.data.get('email', None), ]
            try:
                send_mail(subject, message, email_from, recipient_list)
            except SMTPException:
                raise ValidationError({'message': 'error has occurred while send code on this email'})
            response = HttpResponseRedirect(resolve_url('forgot2'))
            response.set_cookie('restore_email', form.data.get('email'))
            return response  # Redirect to a success page
        else:
            # If the form is invalid, render the form again with errors
            return render(request, self.template_name, {'form': form})


class ForgotCodeView(TemplateView):
    template_name = 'forgot_code.html'
    form_class = RecoveryForm

    def get(self, request, *args, **kwargs):
        restore_email = request.COOKIES.get('restore_email')
        if not restore_email:
            return redirect('forgot1')
        return super(ForgotCodeView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        restore_email = request.COOKIES.get('restore_email')
        if not restore_email:
            return redirect('forgot1')
        tempdict = self.request.POST.copy()
        tempdict['email'] = restore_email
        form = self.form_class(tempdict)
        if form.is_valid():
            new_password = form.data.get('password', None)
            try:
                instance = User.objects.get(email=form.data.get('email'))
            except User.DoesNotExist:
                raise ValidationError('user not found')
            try:
                instance_recovery = UserRecovery.objects.get(user=instance)
            except UserRecovery.DoesNotExist:
                return redirect('forgot1')
            if check_password(form.data.get('code'), instance_recovery.code):
                instance.set_password(new_password)
                instance.save()
                instance_recovery.delete()
            response = HttpResponseRedirect(resolve_url('forgot3'))
            response.delete_cookie('restore_email')
            return response
        else:
            return render(request, self.template_name, {'form': form})


class ForgotSuccessView(TemplateView):
    template_name = 'forgot_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['redirect_url'] = reverse_lazy('main')
        return context
