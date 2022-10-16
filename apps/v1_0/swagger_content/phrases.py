from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers

phrases_decorator = extend_schema_view(
    list=extend_schema(tags=['phrases'], description='список фраз', summary='список фраз'),
    retrieve=extend_schema(tags=['phrases'], description='айди фразы', summary='список фраз'),
    open_today_phrase=extend_schema(tags=['phrases'],
                                    request=None,
                                    description='открыть новую фразу, работает один раз в день для каждого юзера',
                                    summary='открыть фразу'),
    is_opened_today=extend_schema(tags=['phrases'],
                                  request=None,
                                  responses=inline_serializer('IsOpenedSerializer',
                                                              fields={'is_opened': serializers.BooleanField()}),
                                  description='проверка открыта ли сегодня фраза через кнопку',
                                  summary='проверка открыта ли фраза'
                                  ),
    last_opened=extend_schema(tags=['phrases'],
                              request=None,
                              description='последняя открытая фраза',
                              summary='последняя открытая фраза')
)
