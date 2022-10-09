"""ComplimentApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema-admin'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema-admin'), name='swagger-ui'),
    path('api/v1_0/', include('apps.v1_0.urls.all'))
]

# create user +
# login +
# refresh +
# patch user +
# check is created -
# send data to email -
# get list of phrases, filter: my, rarity, left_sharing, is_watched, filter by_date
# create share
# open phrase by link