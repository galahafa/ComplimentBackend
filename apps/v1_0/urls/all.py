from django.urls import include, path
from rest_framework import routers

from apps.v1_0.views.phrases import PhraseViewSet
from apps.v1_0.views.users import MyObtainTokenPairView, MyTokenRefreshView, UserViewSet

router = routers.DefaultRouter()
router.register('phrase', PhraseViewSet, basename='phrase')
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
