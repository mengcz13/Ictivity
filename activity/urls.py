# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-23 09:59:25
# @Last Modified by:   neozero
# @Last Modified time: 2016-05-23 20:38:09
from django.conf.urls import url
from activity import views

urlpatterns = [
    url(r'^create/?$', views.activity_create),
    url(r'^info/?$', views.activity_info),
    url(r'^holdlist/?$', views.activity_holdlist),
    url(r'^joinlist/?$', views.activity_joinlist),
]