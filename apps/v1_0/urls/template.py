from django.urls import path
from apps.v1_0.template_views import users, phrases


urlpatterns = [
    # main process
    path('main/', phrases.IndexView.as_view(), name='main'),
    path('collection/', phrases.CollectionView.as_view(), name='collection'),
    path('phrase/<int:pk>/', phrases.DetailView.as_view(), name='detail'),
    path('share/<int:id>/', phrases.ShareView.as_view(), name='share'),
    path('guide/', phrases.GuideView.as_view(), name='guide'),
    path('get_phrase/<str:id>/', phrases.GetPhraseView.as_view(), name='get_phrase'),
    path('play/', phrases.my_view, name='play'),

    # auth process
    path('login/', users.LoginView.as_view(), name='login'),
    path('start/', users.StartPageView.as_view(), name='start'),
    path('registration/', users.RegistrationView.as_view(), name='registration'),
    path('password_reset/email/', users.ForgotEmailView.as_view(), name='forgot1'),
    path('password_reset/code/', users.ForgotCodeView.as_view(), name='forgot2'),
    path('password_reset/success/', users.ForgotSuccessView.as_view(), name='forgot3'),
    path('profile/', users.ProfileView.as_view(), name='profile'),
    path('logout/', users.LogoutView.as_view(), name='logout')

]
