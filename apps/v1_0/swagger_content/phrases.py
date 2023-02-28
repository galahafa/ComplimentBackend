from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers

phrases_decorator = extend_schema_view(
    list=extend_schema(tags=['phrases'], description='open phrases list', summary='phrases list'),
    retrieve=extend_schema(tags=['phrases'], description='single phrase', summary='single phrase'),
    open_today_phrase=extend_schema(tags=['phrases'],
                                    request=None,
                                    description='open new phrase, work only one time in day for each user',
                                    summary='open new phrase'),
    is_opened_today=extend_schema(tags=['phrases'],
                                  request=None,
                                  responses=inline_serializer('IsOpenedSerializer',
                                                              fields={'is_opened': serializers.BooleanField()}),
                                  description='check if user open phrase today',
                                  summary='check if user open phrase today'
                                  ),
    last_opened=extend_schema(tags=['phrases'],
                              request=None,
                              description='last opened phrase',
                              summary='last opened phrase')
)
