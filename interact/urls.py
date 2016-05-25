# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-23 21:39:41
# @Last Modified by:   neozero
# @Last Modified time: 2016-05-23 21:40:37
from django.conf.urls import url
from interact import views

urlpatterns = [
    url(r'^sign/?$', views.interact_sign),
]