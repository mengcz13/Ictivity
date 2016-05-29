'''
Created on 2016.5.16

@author: llylly
'''

from django.conf.urls import url
import views.user
import views.activity
import view 

urlpatterns = [
    url(r'user/register$', views.user.register, name="api/register"),
    url(r'user/login$', views.user.login, name="api/login"),
    url(r'user/logout$', views.user.logout, name="api/logout"),
    url(r'user/info$', views.user.info, name="api/info"),
    url(r'user/token$', views.user.token, name="api/token"),
    url(r'user/changeinfo', views.user.changeinfo, name="api/changeinfo"),
    url(r'user/changepwd', views.user.changepwd, name="api/changepwd"),
    url(r'user/photos', views.user.photos, name="api/photos"),
    url(r'user/uploadphoto', views.user.uploadphoto, name="api/uploadphoto"),
    
    url(r'activity/holdList$', views.activity.holdList, name="api/holdList"),
    url(r'activity/joinList$', views.activity.joinList, name="api/joinList"),
    url(r'activity/info$', views.activity.info, name="api/activity/info"),
    url(r'activity/ginfo$', views.activity.ginfo, name="api/activity/ginfo"),
    url(r'activity/create$', views.activity.create, name="api/createActivity"),
    url(r'activity/role$', views.activity.role, name="api/role"),
    url(r'activity/join$', views.activity.join, name="api/join"),
    url(r'activity/notices$', views.activity.notices, name="api/notices"),
    url(r'activity/comments$', views.activity.comments, name="api/comments"),
    url(r'activity/members$', views.activity.members, name="api/members"),
    url(r'activity/newComment', views.activity.newComment, name="api/newComment"),
    url(r'activity/newNotice', views.activity.newNotice, name="api/newNotice"),
    
    url(r'search', view.search, name="api/search"),
]