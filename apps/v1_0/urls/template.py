from django.contrib.auth.views import PasswordResetView
from django.urls import path
from apps.v1_0.template_views import users, phrases


urlpatterns = [
    path('main/', phrases.IndexView.as_view(), name='main'),
    path('collection/', phrases.CollectionView.as_view(), name='collection'),
    path('phrase/<int:pk>/', phrases.DetailView.as_view(), name='detail'),
    path('login/', users.LoginView.as_view(), name='login'),
    path('start/', users.StartPageView.as_view(), name='start'),
    path('registration/', users.RegistrationView.as_view(), name='registration'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/email/', users.ForgotEmailView.as_view(), name='forgot1'),
    path('password_reset/code/', users.ForgotCodeView.as_view(), name='forgot2'),
    path('password_reset/success/', users.ForgotSuccessView.as_view(), name='forgot3'),
]
