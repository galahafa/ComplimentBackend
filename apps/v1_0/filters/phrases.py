from django_filters import rest_framework as filters

from apps.models.phrases import Phrase


class PhraseFilters(filters.FilterSet):
    my = filters.BooleanFilter(method='filter_my')
    left_sharing = filters.BaseInFilter(method='filter_left_sharing')
    watched = filters.BooleanFilter(method='filter_watched')

    class Meta:
        model = Phrase
        fields = ['my', 'rarity', 'left_sharing', ]

    def filter_my(self, queryset, name, value):
        if value:
            user = self.request.user
            queryset = queryset.filter(openphrase__user=user)
        return queryset

    def filter_left_sharing(self, queryset, name, value):
        value = value.split(',')
        queryset = queryset.filter(openphrase__left_sharing__in=value)
        return queryset

    def filter_watched(self, queryset, name, value):
        queryset = queryset.filter(openphrase__is_watched=value)
        return queryset
