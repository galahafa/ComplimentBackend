from drf_spectacular.utils import extend_schema, extend_schema_view

users_decorator = extend_schema_view(
    list=extend_schema(tags=['users'], exclude=True),
    create=extend_schema(tags=['users'],
                         description='создание пользователя',
                         summary='регистрация пользователя'),
    update=extend_schema(tags=['users'], exclude=True),
    partial_update=extend_schema(tags=['users'], exclude=True),
    retrieve=extend_schema(tags=['users'], exclude=True),
    my=extend_schema(tags=['users'], description='информация об авторизованном пользователе', methods=['GET'],
                     summary='информация о пользователе'),
    start_recovery=extend_schema(tags=['users'], description='отправить код для восстановления на почту',
                                 summary='начало восстановления пароля'),
    finish_password=extend_schema(tags=['users'], description='восстановить пароль',
                                  summary='конец восстановления пароля'),
)

user_my_decorator = extend_schema(tags=['users'], description='изменение авторизованного пользователя',
                                  methods=['PATCH'], summary='изменение пользователя')
# user_my_decorator_2 = extend_schema(tags=['users'], description='test', methods=['GET']),


token_auth_decorator = extend_schema_view(
    post=extend_schema(tags=['auth'],
                       description='получить токен для авторизации, юзернейм принимает логин или почту',
                       summary='авторизация')
)

token_refresh_decorator = extend_schema_view(
    post=extend_schema(tags=['auth'],
                       description='обновить токен авторизации',
                       summary='обновление токена')
)
