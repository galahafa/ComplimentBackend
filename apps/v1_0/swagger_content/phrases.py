from drf_spectacular.utils import extend_schema, extend_schema_view

phrases_decorator = extend_schema_view(
    list=extend_schema(tags=['phrases']),
    retrieve=extend_schema(tags=['phrases']),
    open_today_phrase=extend_schema(tags=['phrases'],
                                    request=None),
)
