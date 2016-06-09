'''
Created on 2016.5.15

@author: llylly
'''

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    
    url(r'^user/login$', views.login, name="login"),
    url(r'^user/register$', views.register, name="register"),
    url(r'^user/profile$', views.profile, name="profile"),
    
    url(r'^activity/holdList$', views.holdList, name="holdList"),
    url(r'^activity/joinList$', views.joinList, name="joinList"),
    url(r'^activity/newActivity$', views.newActivity, name="newActivity"),
    url(r'^activity$', views.activity, name="activity"),
    
    url(r'^backstage$', views.backstage, name="backstage"),
    
    url(r'^search$', views.search, name="search"),
    
    url(r'^interact/qrcodeshow$', views.qrcodeshow, name="qrcodeshow"),
    url(r'^interact/sign$', views.sign, name="sign"),
    url(r'^interact/signUser$', views.signUser, name="signUser"),
    url(r'^interact/signInfo$', views.signInfo, name="signInfo"),
    url(r'^interact/signError$', views.signError, name="signError"),
    url(r'^interact/signSuccess$', views.signSuccess, name="signSuccess"),
    url(r'^interact/vote$', views.vote, name="vote"),
    url(r'^interact/voteInfo$', views.voteInfo, name="voteInfo"),
    url(r'^interact/voteError$', views.voteError, name="voteError"),
    url(r'^interact/voteSuccess', views.voteSuccess, name="voteSuccess"),
    
    url(r'^prize$', views.prize, name="prize"),
    url(r'^prizeError$', views.prizeError, name="prizeError"),
    
    url(r'^about$', views.about, name="about"),
    
    url(r'^404$', views.page404, name="page404"),
]