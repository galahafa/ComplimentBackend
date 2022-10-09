from django.db import models

from apps.models.phrases import Phrase
from apps.models.users import User


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)


class TagToUser(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TagToPhrase(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
