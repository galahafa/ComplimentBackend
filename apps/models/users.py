from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)


class Friend(models.Model):
    my = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to')
    create_date = models.DateTimeField(auto_now_add=True)
