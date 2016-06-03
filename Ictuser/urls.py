# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-22 19:32:36
# @Last Modified by:   mengcz13
# @Last Modified time: 2016-06-03 19:36:23
from django.conf.urls import url
from Ictuser import views

urlpatterns = [
    url(r'^register/?$', views.Ictuser_register),
    url(r'^login/?$', views.Ictuser_login),
    url(r'^logout/?$', views.Ictuser_logout),
    url(r'^info/?$', views.Ictuser_userinfo),
    url(r'^changeinfo/?$', views.Ictuser_changeinfo),
    url(r'^changepwd/?$', views.Ictuser_changepwd),
    url(r'^token/?$', views.Ictuser_token),
    url(r'^photos/?$', views.Ictuser_photos),
    url(r'^uploadphoto/?$', views.Ictuser_uploadphoto),
]