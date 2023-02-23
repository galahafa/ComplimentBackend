from django.urls import path
from apps.v1_0.template_views import users, phrases


urlpatterns = [
    path('main/', phrases.IndexView.as_view(), name='main'),
    path('collection/', phrases.CollectionView.as_view(), name='collection'),
    path('phrase/<int:pk>/', phrases.DetailView.as_view(), name='detail'),
    path('accounts/login/', users.LoginView.as_view(), name='login'),
]
