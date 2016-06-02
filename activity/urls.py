# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-23 09:59:25
# @Last Modified by:   mengcz13
# @Last Modified time: 2016-05-31 16:19:28
from django.conf.urls import url
from activity import views

urlpatterns = [
    url(r'^create/?$', views.activity_create),
    url(r'^info/?$', views.activity_info),
    url(r'^holdList/?$', views.activity_holdlist),
    url(r'^joinList/?$', views.activity_joinlist),
]