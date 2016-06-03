'''
Created on 2016.5.16

@author: llylly
'''
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

testToken = "ABCDEF123456"

@ensure_csrf_cookie
def register(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
        #means the request method can only be post 
        #or return 1 as error code
    else:
        dict['error_code'] = 200 #means successful
    return JsonResponse(dict)

@ensure_csrf_cookie
def login(request):
    dict = {'error_code':200}
    if request.method != 'POST':
        dict['error_code'] = 201 
        #means the request method can only be post 
        #or return 201 as error code
    else:
        if (request.POST["username"] == "admin") :
            request.session["userId"] = 1 #login
        else:
            dict['error_code'] = 1
        #error_code:1 means username wrong
        #error_code:2 means password wrong

    return JsonResponse(dict)

@ensure_csrf_cookie
def logout(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
        #means the request method can only be post 
        #or return 201 as error code
    else:
        getAccessToken = request.POST.get('access_token', 0);
        if getAccessToken != testToken:
            dict['error_code'] = 1 #means not verified
        else:
            dict['error_code'] = 200
            request.session["userId"] = 0; #logout
    return JsonResponse(dict)

@ensure_csrf_cookie
def info(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
        #means the request method can only be post 
        #or return 201 as error code
    else:
        getAccessToken = request.POST.get('access_token', 0);
        if getAccessToken != testToken: 
            dict['error_code'] = 1 # means not verified
        else:
            dict['error_code'] = 200
            #########
            #below are test_things
            #delete when fulfilling it!
            dict['username'] = 'lamour'
            dict['email'] = 'lll@mails.tsinghua.edu.cn'
            dict['location'] = 'Haidian, Peking'
            dict['birthday'] = '1989.6.4'
            #########
    return JsonResponse(dict)

@ensure_csrf_cookie
def token(request): 
    # new added port for get accessToken
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
        #means the request method can only be post 
        #or return 201 as error code
    else:
        if request.session.get("userId", default = 0) == 0:
            dict['error_code'] = 1 #means not logined in
        else:
            dict['error_code'] = 200
            dict['access_token'] = testToken
    return JsonResponse(dict)

@ensure_csrf_cookie
def changeinfo(request):
    dict = {}
    dict['error_code'] = 200
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        getAccessToken = request.POST.get('access_token', 0);
        if getAccessToken != testToken:
            dict['error_code'] = 1 #means not verified
        else:
            email = request.POST.get('email', 0)
            location = request.POST.get('location', 0)
            birthday = request.POST.get('birthday', 0)
            if (email == 0) or (location == 0) or (birthday == 0):
                dict['error_code'] = 2 #means info incomplete
            else:
                dict['error_code'] = 200 #means successful saved
    return JsonResponse(dict)

@ensure_csrf_cookie
def changepwd(request):
    dict = {}
    dict['error_code'] = 200
    if request.method != 'POST':
        dict['error_code'] = 201
    else: 
        getAccessToken = request.POST.get('access_token', 0);
        if getAccessToken != testToken:
            dict['error_code'] = 1 #means not verified
        else:
            newpwd = request.POST.get('newpwd', 0)
            if newpwd == 0:
                dict['error_code'] = 2 #means info incomplete
            else:
                if request.POST.get('oldpwd', 0) != "123456":
                    dict['error_code'] = 3 #means old password is wrong
    return JsonResponse(dict)

@ensure_csrf_cookie
def photos(request):
    dict = {}
    dict['error_code'] = 200
    if request.method != 'POST':
        dict['error_code'] = 201
    else: 
        getAccessToken = request.POST.get('access_token', 0);
        if getAccessToken != testToken:
            dict['error_code'] = 1 #means not verified
        else:
            p1 = {'url':'/media/photos/1.jpg', 'time':'2016.5.3 22:21:20'}
            p2 = {'url':'/media/photos/2.jpg', 'time':'2016.5.4 12:59:01'}
            photos = [p1, p2]
            dict['photos'] = photos
    return JsonResponse(dict)

@ensure_csrf_cookie
def uploadphoto(request):
    dict = {}
    dict['error_code'] = 200
    if request.method != 'POST':
        dict['error_code'] = 201
    else: 
        getAccessToken = request.POST.get('access_token', 0);
        if getAccessToken != testToken:
            dict['error_code'] = 1 #means not verified
        else:
            photo = request.FILES.get('photo', "")
            if (photo == "") or (photo.size == 0):
                dict['error_code'] = 2 #means incomplete
            else:
                dict['error_code'] = 200
    return JsonResponse(dict)
