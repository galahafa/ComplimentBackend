from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.utils.text import capfirst

from apps.models import User

UserModel = get_user_model()


class LoginForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username',
                                                             'placeholder': 'username'}))
    # email = forms.CharField(widget=forms.TextInput(attrs={'class': 'email',
    #                                                       'placeholder': 'email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'password',
                                                             'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    username = UsernameField(widget=forms.TextInput(attrs={'class': 'username',
                                                           'placeholder': 'username'}))
    password = forms.CharField(
        # label=_("Password"),
        strip=False,
        widget=forms.TextInput(attrs={'class': 'password',
                                      'placeholder': 'password'}),
    )

    error_messages = {
        "invalid_login":
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ,
        "inactive": "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )


class RegistrationForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username',
                                                             'placeholder': 'username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'email',
                                                          'placeholder': 'email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'password',
                                                             'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
