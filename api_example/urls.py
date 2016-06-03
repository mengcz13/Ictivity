'''
Created on 2016.5.16

@author: llylly
'''

from django.conf.urls import url
import views.user
import views.activity
import views.interact
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
    url(r'activity/editInfo', views.activity.editInfo, name="api/editInfo"),
    url(r'activity/verifyList', views.activity.verifyList, name="api/verifyList"),
    url(r'activity/verifyReject', views.activity.verifyReject, name="api/verifyReject"),
    url(r'activity/verifyPass', views.activity.verifyPass, name="api/verifyPass"),
    
    url(r'interact/createSign', views.interact.createSign, name="api/createSign"),
    url(r'interact/signList', views.interact.signList, name="api/signList"),
    url(r'interact/signed', views.interact.signed, name="api/signed"),
    url(r'interact/msigned', views.interact.msigned, name="api/msigned"),
    url(r'interact/signInfo', views.interact.signInfo, name="api/signInfo"),
    url(r'interact/createVote', views.interact.createVote, name="api/createVote"),
    url(r'interact/signurl', views.interact.signurl, name="api/signurl"),
    url(r'interact/voteurl', views.interact.voteurl, name="api/voteurl"),
    
    url(r'search', view.search, name="api/search"),
]