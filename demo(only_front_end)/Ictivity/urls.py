"""Ictivity URL Configuration

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
from django.conf.urls import url
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls.static import serve
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from app import urls as app_urls
from api import urls as api_urls
from settings import STATIC_ROOT
from settings import MEDIA_ROOT

urlpatterns = [
    url(r'^', include(app_urls.urlpatterns)),
    url(r'^api/', include(api_urls.urlpatterns)),
    url(r'^admin/', admin.site.urls),
    url(r'^static/(.*)$', serve, {'document_root':STATIC_ROOT}),
    url(r'^media/(.*)$', serve, {'document_root':MEDIA_ROOT}),
]

