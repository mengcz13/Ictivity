from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.conf.global_settings import CSRF_COOKIE_AGE
import random

testToken = "ABCDEF123456"

@ensure_csrf_cookie
def search(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('wd', "") != ""):
            ids = [1,4,5,7,6,3]
            dict["ids"] = ids
    return JsonResponse(dict)

@ensure_csrf_cookie
def command(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', -1) != testToken):
            dict['ids'] = []
            for i in range(1, 10):
                dict['ids'].append(int(random.uniform(1, 100)))
        else:
            dict['ids'] = [1,3,5,7,9,11,13,15,17,19]
    return JsonResponse(dict)
