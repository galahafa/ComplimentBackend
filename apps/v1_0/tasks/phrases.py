import random

from celery import shared_task

from apps.common_utils.functions import get_rarity
from apps.models import User
from apps.models.phrases import OpenPhrase, Phrase


@shared_task
def start_opening():
    users = User.objects.filter(is_active=True)
    for user in users:
        open_phrase.delay(user.id)


@shared_task
def open_phrase(user_id):
    rarity = get_rarity()
    phrases = Phrase.objects.filter(user_id=user_id, rarity=rarity).exclude(openphrase__user_id=user_id)
    count = phrases.count()
    random_phrase = phrases[random.randint(0, count - 1)]
    OpenPhrase.objects.create(phrase_id=random_phrase, user_id=user_id)
    # notifications here
