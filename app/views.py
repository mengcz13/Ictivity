from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

@cache_page(60 * 5)

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'user/login.html')

def register(request):
    return render(request, 'user/register.html')

def profile(request):
    return render(request, 'user/profile.html')

def holdList(request):
    return render(request, 'activity/holdList.html')

def joinList(request):
    return render(request, 'activity/joinList.html')

def newActivity(request):
    return render(request, 'activity/newActivity.html')

def activity(request):
    return render(request, 'activity.html')

def backstage(request):
    return render(request, 'backstage.html')

def search(request):
    return render(request, 'search.html')

def page404(request):
    return render(request, '404.html')

def qrcodeshow(request):
    return render(request, 'interact/qrcodeshow.html')

def sign(request):
    return render(request, 'interact/sign.html')

def signUser(request):
    return render(request, 'interact/signUser.html')

def signInfo(request):
    return render(request, 'interact/signInfo.html')

def signError(request):
    return render(request, 'interact/signError.html')

def signSuccess(request):
    return render(request, 'interact/signSuccess.html')

def vote(request):
    return render(request, 'interact/vote.html')

def voteInfo(request):
    return render(request, 'interact/voteInfo.html')

def voteError(request):
    return render(request, 'interact/voteError.html')

def voteSuccess(request):
    return render(request, 'interact/voteSuccess.html')

def prize(request):
    return render(request, 'prize.html')

def prizeError(request):
    return render(request, 'prizeError.html')

def about(request):
    return render(request, 'about.html')

