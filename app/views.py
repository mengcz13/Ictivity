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