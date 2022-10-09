from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models.users import User
from apps.v1_0.serializers.users import MyTokenObtainPairSerializer, UserSerializer
from apps.v1_0.swagger_content.users import users_decorator


@users_decorator
class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        serializer_class = UserSerializer
        return serializer_class


class MyObtainTokenPairView(TokenObtainPairView):
    # permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
