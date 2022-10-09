from drf_spectacular.utils import extend_schema, extend_schema_view

users_decorator = extend_schema_view(
    list=extend_schema(tags=['users']),
    create=extend_schema(tags=['users']),
    update=extend_schema(tags=['users']),
    partial_update=extend_schema(tags=['users']),
    retrieve=extend_schema(tags=['users']),
    phrase=extend_schema(tags=['users']),
    tag=extend_schema(tags=['users'], request=None),
    destroy=extend_schema(tags=['users'])
)
