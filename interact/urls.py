# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-23 21:39:41
# @Last Modified by:   mengcz13
# @Last Modified time: 2016-06-04 01:56:22
from django.conf.urls import url
from interact import views

urlpatterns = [
    url(r'^createSign/?$', views.interact_createSign),
    url(r'^signList/?$', views.interact_signList),
    url(r'^msigned/?$', views.interact_msigned),
    url(r'^signed/?$', views.interact_signed),
    url(r'^signInfo/?$', views.interact_signinfo),
    url(r'^signurl/?$', views.interact_signurl),
    url(r'^signTimeVerify/?$', views.interact_signTimeVerify),
    url(r'^sign/?$', views.interact_sign),
]