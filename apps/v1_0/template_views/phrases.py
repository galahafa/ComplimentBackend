from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db.models import Exists, F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from rest_framework.exceptions import ValidationError as RestValidationError
from apps.models.phrases import Collection, Phrase, OpenPhrase
from apps.v1_0.serializers.phrases import OpenNewPhraseSerializer


class IndexView(UserPassesTestMixin, generic.ListView):
    template_name = 'main_process/index.html'
    context_object_name = 'phrases_list'
    login_url = 'start'

    def test_func(self):
        return self.request.user.is_authenticated

    def is_opened_today(self, request):
        user = request.user
        queryset = self.get_queryset()
        today = timezone.now()
        print(today.day, today.month, today.year)
        queryset = queryset.filter(openphrase__user=user,
                                   openphrase__open_date__year=today.year,
                                   openphrase__open_date__month=today.month,
                                   openphrase__open_date__day=today.day,
                                   # openphrase__get_from=None
                                   )
        print(queryset)
        if queryset:
            response_message = {'is_opened': True}
        else:
            response_message = {'is_opened': False}
        if response_message.get('is_opened'):
            queryset = self.get_queryset()
            queryset = queryset.filter(openphrase__user=user).order_by('-openphrase__open_date').first()
            response_message['phrase'] = queryset
        return response_message

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'today_phrase': self.is_opened_today(request=self.request)
        })
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        qs = Phrase.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseRedirect('start')
        return super(IndexView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = OpenNewPhraseSerializer(data={'user': user.id})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return HttpResponseRedirect("/main/")
        except RestValidationError as e:
            context = {}
            context['errors'] = e.detail
            return render(request, self.template_name, context=context)


class DetailView(generic.DetailView):
    model = Phrase
    template_name = 'detail.html'


class ShareView(generic.TemplateView):
    template_name = 'share_phrase.html'
    model = Phrase

    def get_context_data(self, **kwargs):
        context = super(ShareView, self).get_context_data(**kwargs)
        phrase_id = self.kwargs.get('id')
        user = self.request.user
        try:
            open_phrase = OpenPhrase.objects.get(phrase_id=phrase_id, user=user)
        except OpenPhrase.DoesNotExist:
            raise ValidationError({'phrase': 'you do not have access for this phrase yet, try next time'})
        base_url = 'http://10.0.0.191:8000/get_phrase/'
        context.update({
            'share_url': f'{base_url}?p={open_phrase.id}',
            'share_text': 'Hi, I have compliment for you'
        })
        return context


class GuideView(generic.TemplateView):
    template_name = 'guide.html'


class CollectionView(generic.ListView):
    template_name = 'main_process/collection.html'
    context_object_name = 'phrases_list'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        context.update({
            'collections': Collection.objects.all(),
            'phrase_number': Phrase.objects.all().count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        qs = Phrase.objects.all().annotate(is_watched=F('openphrase__is_watched'),
                                           is_get=Exists(OpenPhrase.objects.filter(user=user))).distinct()
        return qs


class GetPhraseView(generic.TemplateView):
    template_name = 'get_shared_phrase.html'

    #

    def is_opened_today(self, request):
        user = request.user
        queryset = self.get_queryset()
        today = timezone.now()
        queryset = queryset.filter(openphrase__user=user,
                                   openphrase__open_date__year=today.year,
                                   openphrase__open_date__month=today.month,
                                   openphrase__open_date__day=today.day,
                                   openphrase__get_from=None
                                   )
        if queryset:
            response_message = {'is_opened': True}
        else:
            response_message = {'is_opened': False}
        if response_message.get('is_opened'):
            queryset = self.get_queryset()
            queryset = queryset.filter(openphrase__user=user).order_by('-openphrase__open_date').first()
            response_message['phrase'] = queryset
        return response_message

    def get_context_data(self, **kwargs):
        context = super(GetPhraseView, self).get_context_data(**kwargs)
        phrase_id = self.kwargs.get('id')
        user = self.request.user
        try:
            open_phrase = OpenPhrase.objects.get(id=phrase_id)
        except OpenPhrase.DoesNotExist:
            context.update({'check_phrase': {'status': 'error', 'message': 'this phrase not found'}})
            return context
        test = OpenPhrase.objects.filter(phrase=open_phrase.phrase, user=user)
        if (user.is_authenticated and
                (open_phrase.user == user or
                 test.exists())):
            context.update({'check_phrase': {'status': 'error', 'message': 'you already have this phrase'},
                            'open_phrase': test.first()})
        else:
            context.update({
                'check_phrase': {'status': 'success'},
                'open_phrase': open_phrase
            })
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        phrase_id = self.kwargs.get('id')
        serializer = OpenNewPhraseSerializer(data={'user': user.id, 'from_phrase': phrase_id})
        try:
            serializer.is_valid(raise_exception=False)
            serializer.save()
            return HttpResponseRedirect(f"/get_phrase/{phrase_id}/" + "?success=true")
        except RestValidationError as e:
            context = {}
            context['errors'] = e.detail
            return render(request, self.template_name, context=context)


def my_view(request):
    cards = [
        {'title': 'Card 1', 'text': 'This is the text for card 1.'},
        {'title': 'Card 2', 'text': 'This is the text for card 2.'},
        {'title': 'Card 3', 'text': 'This is the text for card 3.'},
        {'title': 'Card 4', 'text': 'This is the text for card 4.'},
        {'title': 'Card 5', 'text': 'This is the text for card 5.'},
        {'title': 'Card 1', 'text': 'This is the text for card 1.'},
        {'title': 'Card 2', 'text': 'This is the text for card 2.'},
        {'title': 'Card 3', 'text': 'This is the text for card 3.'},
        {'title': 'Card 4', 'text': 'This is the text for card 4.'},
        {'title': 'Card 5', 'text': 'This is the text for card 5.'},
        {'title': 'Card 1', 'text': 'This is the text for card 1.'},
        {'title': 'Card 2', 'text': 'This is the text for card 2.'},
        {'title': 'Card 3', 'text': 'This is the text for card 3.'},
        {'title': 'Card 4', 'text': 'This is the text for card 4.'},
        {'title': 'Card 5', 'text': 'This is the text for card 5.'},

    ]
    return render(request, 'play.html', {'cards': cards})
