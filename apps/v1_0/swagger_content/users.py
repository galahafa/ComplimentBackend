from drf_spectacular.utils import extend_schema, extend_schema_view

users_decorator = extend_schema_view(
    list=extend_schema(tags=['users'], exclude=True),
    create=extend_schema(tags=['users'],
                         description='create user',
                         summary='user registration'),
    update=extend_schema(tags=['users'], exclude=True),
    partial_update=extend_schema(tags=['users'], exclude=True),
    retrieve=extend_schema(tags=['users'], exclude=True),
    my=extend_schema(tags=['users'], description='information about auth user', methods=['GET'],
                     summary='user information'),
    start_recovery=extend_schema(tags=['users'], description='send recovery code to email',
                                 summary='start password recovery'),
    finish_password=extend_schema(tags=['users'], description='restore password',
                                  summary='finish password recovery'),
)

user_my_decorator = extend_schema(tags=['users'], description='change auth user',
                                  methods=['PATCH'], summary='change user')
# user_my_decorator_2 = extend_schema(tags=['users'], description='test', methods=['GET']),


token_auth_decorator = extend_schema_view(
    post=extend_schema(tags=['auth'],
                       description='get token for authorization, username field take username or email',
                       summary='auth')
)

token_refresh_decorator = extend_schema_view(
    post=extend_schema(tags=['auth'],
                       description='refresh auth token',
                       summary='refresh token')
)

error_docs_decorator = extend_schema_view(
    get=extend_schema(tags=['docs'],
                      description='error list',
                      summary='dict of all error code')
)
