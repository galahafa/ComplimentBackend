import uuid

from django.db import models

from apps.models.users import User

RARITY = [
    (1, "common"),
    (2, "uncommon"),
    (3, "rare"),
    (4, "mythical"),
    (5, "legendary")
]

STATUSES = (
    (1, 'Published'),
    (0, 'BackLog')
)


class Collection(models.Model):
    name = models.CharField(max_length=256)
    status = models.IntegerField(choices=STATUSES, default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name[:30]


class Phrase(models.Model):
    text = models.CharField(max_length=1024)
    rarity = models.IntegerField(choices=RARITY, default=1)
    status = models.IntegerField(choices=STATUSES, default=1)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, null=True, blank=True, default=None)

    def __str__(self):
        return self.text[:50]


class OpenPhrase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    open_date = models.DateTimeField(auto_now_add=True)
    is_watched = models.BooleanField(default=True)
    get_from = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='get_from',
                                 null=True, blank=True, default=None)
    left_to_share = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.phrase.text} to {self.user.id}'
