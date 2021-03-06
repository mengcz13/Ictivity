"""ictivity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import serve
from django.contrib.auth.models import User
from app import urls as app_urls
from ictivity import views
from settings import STATIC_ROOT
from settings import MEDIA_ROOT


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/user/', include('Ictuser.urls')),
    url(r'^api/activity/', include('activity.urls')),
    url(r'^api/interact/', include('interact.urls')),
    url(r'^api/search/?$', views.search),
    url(r'^api/command/?$', views.command),

    url(r'^', include(app_urls.urlpatterns)),
    url(r'^static/(.*)$', serve, {'document_root':STATIC_ROOT}),
    url(r'^media/(.*)$', serve, {'document_root':MEDIA_ROOT})
]
