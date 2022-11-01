from django.urls import include, path, re_path

from apps.common_utils.routers import CustomDefaultRouter
from apps.v1_0.views.phrases import PhraseViewSet
from apps.v1_0.views.users import MyObtainTokenPairView, MyTokenRefreshView, UserViewSet

router = CustomDefaultRouter()
router.register('phrase', PhraseViewSet, basename='phrase')
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'login/?', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    re_path(r'login/refresh/?', MyTokenRefreshView.as_view(), name='token_refresh'),
]
