from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.models.tags import Tag
from apps.v1_0.serializers.tags import TagSerializer
from apps.v1_0.swagger_content.tags import tags_decorator


@tags_decorator
class TagViewSet(ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=False, methods=['get'])
    def my(self, request, check, *args, **kwargs):
        user = request.user
        qs = self.queryset.filter(tagtouser__user=user)
        serializer = TagSerializer(qs, many=True)
        return Response(serializer.data)
