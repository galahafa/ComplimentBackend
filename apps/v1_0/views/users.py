from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common_utils.viewsets import UserModelViewSet
from apps.models.users import User
from apps.v1_0.serializers.users import (MyTokenObtainPairSerializer, UserFinishRecoverySerializer, UserSerializer,
                                         UserShortSerializer, UserStartRecoverySerializer)
from apps.v1_0.swagger_content.users import (error_docs_decorator, token_auth_decorator, token_refresh_decorator,
                                             user_my_decorator, users_decorator)


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
        elif self.action == 'start_recovery':
            serializer_class = UserStartRecoverySerializer
        elif self.action == 'finish_password':
            serializer_class = UserFinishRecoverySerializer
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

    @action(methods=['POST'], detail=False)
    def start_recovery(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def finish_password(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        auth = MyTokenObtainPairSerializer(data={'password': request.data.get('password'),
                                                 'username': serializer.data.get('username')})
        auth.is_valid(raise_exception=True)
        return Response({'instance': serializer.data, 'access': auth.validated_data.get('access'),
                         'refresh': auth.validated_data.get('access')},
                        status=status.HTTP_201_CREATED, headers=headers)


@token_auth_decorator
class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@token_refresh_decorator
class MyTokenRefreshView(TokenRefreshView):
    pass


@error_docs_decorator
class InformationErrorApiView(APIView):

    def get(self, request, *args, **kwargs):
        error_dict = {
            0: 'unrecognized error',
            1: 'base error without type',
            2: 'validation error, most common exception called when incorrect data',
            3: 'error parsing input data',
            4: 'authentication error, called when auth not provided (401 error)',
            5: 'authentication validation error (401 error)',
            6: 'permission error, not enough access (403 error)',
            7: 'object not found (404 error)',
            8: 'REST method not allowed (405 error)',
            9: 'passed not acceptable headers (406 error)',
            10: 'unsupported media type (415 error)',
            11: 'too many request (429 error)'
        }
        return Response(error_dict)
