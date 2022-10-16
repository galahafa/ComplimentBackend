from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common_utils.viewsets import UserModelViewSet
from apps.models.users import User
from apps.v1_0.serializers.users import MyTokenObtainPairSerializer, UserSerializer, UserShortSerializer
from apps.v1_0.swagger_content.users import (token_auth_decorator, token_refresh_decorator, user_my_decorator,
                                             users_decorator)


@users_decorator
class UserViewSet(UserModelViewSet):

    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_permissions(self):
        if self.action == 'my':
            return [IsAuthenticated()]
        elif self.action in ['retrieve', 'partial_update']:
            return [IsAdminUser()]
        return []

    def get_object(self):
        if self.action == 'my':
            return self.get_user_object()
        return super(UserViewSet, self).get_object()

    def get_user_object(self):
        obj = self.request.user
        return obj

    def get_serializer_class(self):
        if self.action == 'my':
            serializer_class = UserShortSerializer
        else:
            serializer_class = UserSerializer
        return serializer_class

    @user_my_decorator
    @action(methods=['GET', 'PATCH'], detail=False)
    def my(self, request, *args, **kwargs):
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        if request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)


@token_auth_decorator
class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@token_refresh_decorator
class MyTokenRefreshView(TokenRefreshView):
    pass
