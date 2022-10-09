from drf_spectacular.utils import extend_schema, extend_schema_view

tags_decorator = extend_schema_view(
    list=extend_schema(tags=['tags']),
    create=extend_schema(tags=['tags']),
    update=extend_schema(tags=['tags']),
    partial_update=extend_schema(tags=['tags']),
    retrieve=extend_schema(tags=['tags']),
    my=extend_schema(tags=['tags']),
    destroy=extend_schema(tags=['tags'])

)
