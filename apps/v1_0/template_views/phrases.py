import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Exists, F
from django.http import HttpResponseRedirect
from django.views import generic

from apps.models.phrases import Collection, Phrase, OpenPhrase
# from apps.v1_0.forms.users import LoginForm


class IndexView(UserPassesTestMixin, generic.ListView   ):
    template_name = 'index.html'
    context_object_name = 'phrases_list'
    login_url = 'start'

    def test_func(self):
        return self.request.user.is_authenticated

    def is_opened_today(self, request):
        user = request.user
        queryset = self.get_queryset()
        today = datetime.datetime.today()
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

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'collections': Collection.objects.all(),
            'today_phrase': self.is_opened_today(request=self.request)
        })
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        user = self.request.user
        qs = Phrase.objects.all().annotate(is_watched=F('openphrase__is_watched'),
                                           is_get=Exists(OpenPhrase.objects.filter(user=user))).distinct()
        return qs

    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseRedirect('start')
        return super(IndexView, self).get(request, *args, **kwargs)


class DetailView(generic.DetailView):
    model = Phrase
    template_name = 'detail.html'


class CollectionView(generic.ListView):
    template_name = 'collection.html'
    context_object_name = 'phrases_list'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        context.update({
            'collections': Collection.objects.all()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        qs = Phrase.objects.all().annotate(is_watched=F('openphrase__is_watched'),
                                           is_get=Exists(OpenPhrase.objects.filter(user=user))).distinct()
        return qs
