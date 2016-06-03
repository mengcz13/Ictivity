# -*- coding: utf-8 -*-
# @Author: neozero
# @Date:   2016-05-23 09:59:25
# @Last Modified by:   mengcz13
# @Last Modified time: 2016-06-03 23:33:10
from django.conf.urls import url
from activity import views

urlpatterns = [
    url(r'^create/?$', views.activity_create),
    url(r'^info/?$', views.activity_info),
    url(r'^ginfo/?$', views.activity_ginfo),
    url(r'^editInfo/?$', views.activity_editinfo),
    url(r'^holdList/?$', views.activity_holdlist),
    url(r'^joinList/?$', views.activity_joinlist),
    url(r'^role/?$', views.activity_role),
    url(r'^join/?$', views.activity_join),
    url(r'^notices/?$', views.activity_notices),
    url(r'^comments/?$', views.activity_comments),
    url(r'^members/?$', views.activity_members),
    url(r'^newComment/?$', views.activity_newcomment),
    url(r'^newNotice/?$', views.activity_newnotice),
    url(r'^verifyList/?$', views.activity_verifyList),
    url(r'^verifyReject/?$', views.activity_verifyReject),
    url(r'^verifyPass/?$', views.activity_verifyPass),
]