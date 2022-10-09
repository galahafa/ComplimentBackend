from django.db.models import Exists, F
from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.models.phrases import OpenPhrase, Phrase
from apps.v1_0.filters.phrases import PhraseFilters
from apps.v1_0.serializers.phrases import OpenNewPhraseSerializer, PhraseListSerializer
from apps.v1_0.swagger_content.phrases import phrases_decorator


@phrases_decorator
class PhraseViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):

    http_method_names = ['get', 'head', 'options', 'post']
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PhraseFilters

    def get_serializer_class(self):
        if self.action == 'open_today_phrase':
            serializer_class = OpenNewPhraseSerializer
        else:
            serializer_class = PhraseListSerializer
        return serializer_class

    def get_queryset(self):
        user = self.request.user
        queryset = Phrase.objects.all().annotate(is_watched=F('openphrase__is_watched'),
                                                 is_get=Exists(OpenPhrase.objects.filter(user=user))).distinct()
        return queryset

    @action(methods=['POST'], detail=False)
    def open_today_phrase(self, request):
        user = request.user
        serializer = self.get_serializer(data={'user': user.id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({'message': 'check'}, status=status.HTTP_400_BAD_REQUEST)
