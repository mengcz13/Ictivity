# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-22 19:32:36
# @Last Modified by:   neozero
# @Last Modified time: 2016-05-22 21:16:35
from django.conf.urls import url
from Ictuser import views

urlpatterns = [
    url(r'^register/?$', views.Ictuser_register),
    url(r'^login/?$', views.Ictuser_login),
    url(r'^logout/?$', views.Ictuser_logout),
    url(r'^info/?$', views.Ictuser_userinfo),
]