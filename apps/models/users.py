from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={"unique": "A user with that username already exists."},
    )
    name = models.CharField(max_length=128, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=128, null=True, blank=True, default=None)
    birthday = models.DateField(default=None, null=True, blank=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)


class Friend(models.Model):
    my = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to')
    create_date = models.DateTimeField(auto_now_add=True)


class UserRecovery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=128)
