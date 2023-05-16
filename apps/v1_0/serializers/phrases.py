import datetime
import random

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError

from apps.common_utils.constant import ERROR_TEXT
from apps.common_utils.functions import get_rarity
from apps.models.phrases import OpenPhrase, Phrase


class PhraseListSerializer(serializers.ModelSerializer):
    is_watched = serializers.BooleanField()
    is_get = serializers.BooleanField()

    class Meta:
        model = Phrase
        fields = '__all__'


class PhraseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrase
        fields = ['id', 'text', 'rarity']


class OpenNewPhraseSerializer(serializers.ModelSerializer):
    phrase = PhraseShortSerializer(read_only=True)
    from_phrase = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = OpenPhrase
        fields = ['user', 'phrase', 'from_phrase']

    def validate(self, attrs):
        today = timezone.now()
        check = OpenPhrase.objects.filter(open_date__year=today.year,
                                          open_date__month=today.month,
                                          open_date__day=today.day,
                                          get_from=None,
                                          user=attrs.get('user'))
        if check:
            raise ValidationError({'phrase': ERROR_TEXT.get('today_opened')})
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        rarity = get_rarity()
        if validated_data.get('from_phrase'):
            try:
                from_phrase = OpenPhrase.objects.get(id=validated_data.get('from_phrase'))
                if from_phrase.left_to_share <= 0:
                    raise ValidationError({'from_phrase': ERROR_TEXT.get('left_share')})
            except OpenPhrase.DoesNotExist:
                raise ValidationError({'from_phrase': 'this phrase not found'})
            instance = OpenPhrase.objects.create(phrase=from_phrase.phrase, user=user, get_from=from_phrase.user)
            from_phrase.left_to_share -= 1
            from_phrase.save()
        else:
            phrases = Phrase.objects.filter(rarity=rarity).exclude(openphrase__user_id=user)

            count = phrases.count()
            if not count:
                phrases = Phrase.objects.exclude(openphrase__user_id=user)
                count = phrases.count()
                if not count:
                    raise ValidationError({'phrase': ERROR_TEXT.get('all_opened')})
            random_phrase = phrases[random.randint(0, count - 1)]
            instance = OpenPhrase.objects.create(phrase=random_phrase, user=user)
        return instance
