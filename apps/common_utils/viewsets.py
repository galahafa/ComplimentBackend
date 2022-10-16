from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class UserModelViewSet(mixins.CreateModelMixin, GenericViewSet, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin):
    pass
