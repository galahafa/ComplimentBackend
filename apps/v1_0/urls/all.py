from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from apps.v1_0.views.phrases import PhraseViewSet
from apps.v1_0.views.users import MyObtainTokenPairView, UserViewSet

router = routers.DefaultRouter()
router.register('phrase', PhraseViewSet, basename='phrase')
router.register('user', UserViewSet)
# router.register('tag', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
