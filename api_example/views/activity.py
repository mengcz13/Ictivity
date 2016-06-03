'''
Created on 2016.5.21

@author: llylly
'''
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

testToken = "ABCDEF123456"

@ensure_csrf_cookie
def holdList(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            actList = []
            for i in range(1, 10, 2):
                actList.append({'id': i})
                dict['ids'] = actList
    return JsonResponse(dict)
    
def joinList(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            actList = []
            for i in range(2, 10, 2):
                actList.append({'id': i})
                dict['ids'] = actList
    return JsonResponse(dict)
    
def info(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            id = (int)(request.POST.get("id", 0))
            ##########
            # below are just for testing
            if ((id <= 0) or (id > 10)):
                dict['error_code'] = 2 # means invalid activity_id
            else:
                dict['id'] = id
                dict['name'] = 'Test Activity ' + str(id)
                dict['tags'] = ['test', 'example']
                dict['description'] = 'goddawn such many banists and magician obsessed with drugs'
                dict['count'] = int(random.uniform(10,100))
                dict['ispublic'] = ((id % 4) >=2)
                dict['isverify'] = ((id % 3) >=1)
            ##########
    return JsonResponse(dict)

def ginfo(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        id = (int)(request.POST.get("id", 0))
        ##########
        # below are just for testing
        if ((id > 7) or (id <= 0)):
            dict['error_code'] = 2 # means invalid activity_id
        else:
            dict['id'] = id
            dict['name'] = 'Test Activity ' + str(id)
            dict['tags'] = ['test', 'example']
            dict['description'] = 'goddawn such many banists and magician obsessed with drugs'
            dict['count'] = int(random.uniform(10,100))
            dict['ispublic'] = ((id % 4) >=2)
            dict['isverify'] = ((id % 3) >=1)
        ##########
    return JsonResponse(dict)
    
def create(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            name = request.POST.get("name", 0)
            tags = request.POST.get("tags", 0)
            description = request.POST.get("description", 0)
            isPublic = request.POST.get("ispublic", -1)
            isVerify = request.POST.get("isverify", -1)
            if ((name == 0) or (isPublic == -1) or (isVerify == -1)):
                dict['error_code'] = 2 #errorcode:2 information lack
            ### this random is just for test return value
            dict['_id'] = int(random.uniform(10, 20))
            ######
    return JsonResponse(dict)

def role(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict["error_code"] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            ### below are just for testing ###
            ##########
            if (id <= 0) or (id >= 10):
                dict['error_code'] = 2 #means invalid activity id
            else:
                if (id <= 3): 
                    dict['role'] = 0
                elif (id <= 6):
                    dict['role'] = 1
                else:
                    dict['role'] = 2
    return JsonResponse(dict)

def join(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict["error_code"] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        elif (id == 0):
            dict['error_code'] = 2 #invalid activity id
        else:
            joinMsg = request.POST.get('join_msg', 0);
            if (joinMsg == 0):
                dict['error_code'] = 3 #invalid join message
    return JsonResponse(dict)

def notices(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        elif (id == 0):
            dict['error_code'] = 2 #invalid activity id
        else:
            noticeList = [];
            for i in range(1, 10):
                noticeList.append({'title': "Test Title" + str(i), 'text':"Test Notice " + str(i), 'time':"2016-5-29 13:00:00"})
            dict['notices'] = noticeList
    return JsonResponse(dict)

def comments(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        elif (id == 0):
            dict['error_code'] = 2 #invalid activity id
        else:
            noticeList = [];
            for i in range(1, 10):
                noticeList.append({'text':"Digital Design is a good course " + str(i), 
                                   'nickname':"Zhao Youjian",
                                   'time':"2016-5-29 14:00:00"})
            dict['comments'] = noticeList
    return JsonResponse(dict)

def members(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        elif (id == 0):
            dict['error_code'] = 2 #invalid activity id
        else:
            members = [];
            for i in range(1, 100):
                members.append({"id": i, "nickname": "testUser" + str(i), "ismanager": bool(i % 3 == 0)});
            dict['members'] = members
    return JsonResponse(dict)

def newComment(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        elif (id == 0):
            dict['error_code'] = 2 #invalid activity id
        else:
            comment = request.POST.get("comment", 0);
            if (comment == 0):
                dict['error_code'] = 3 # no legal comment received
    return JsonResponse(dict)

def newNotice(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        id = (int)(request.POST.get("id", 0))
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        elif (id == 0):
            dict['error_code'] = 2 #invalid activity id
        else:
            notice = request.POST.get("notice", 0)
            title = request.POST.get("title", 0)
            if (notice == 0):
                dict['error_code'] = 3 # no legal notice received
            if (title == 0):
                dict['error_code'] = 4 # no legal title received
    return JsonResponse(dict)
        
def editInfo(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            id = request.POST.get("id", 0)
            tags = request.POST.get("tags", 0)
            description = request.POST.get("description", 0)
            isPublic = request.POST.get("ispublic", -1)
            isVerify = request.POST.get("isverify", -1)
            if ((id == 0) or (isPublic == -1) or (isVerify == -1)):
                dict['error_code'] = 2 #errorcode:2 information lack
    return JsonResponse(dict)

def verifyList(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            if (request.POST.get("act_id", 0) == 0):
                dict['error_code'] = 2 #invalid activity id
            else:
                list = []
                for i in range(1, 10):
                    list.append({"id": int(random.uniform(10, 100)), "msg": "I want to join this activity. My father is Li Gang!"})
                dict['list'] = list
    return JsonResponse(dict)

def verifyReject(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            if (request.POST.get("act_id", 0) == 0) or (request.POST.get("id", 0) == 0):
                dict['error_code'] = 2 #invalid activity id or userid
    return JsonResponse(dict)
    
    
def verifyPass(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            if (request.POST.get("act_id", 0) == 0) or (request.POST.get("id", 0) == 0):
                dict['error_code'] = 2 #invalid activity id or userid
    return JsonResponse(dict)
    
    
