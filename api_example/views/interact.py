'''
Created on 2016.5.30

@author: llylly
'''
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

testToken = "ABCDEF123456"

@ensure_csrf_cookie
def createSign(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get("act_id", -1) == -1):
                legal = False
            if (request.POST.get("name", -1) == -1):
                legal = False
            if (request.POST.get("timeL", -1) == -1):
                legal = False
            if (request.POST.get("timeR", -1) == -1):
                legal = False
            if (request.POST.get("command", -1) == -1):
                legal = False
            if (request.POST.get("isface", -1) == -1):
                legal = False
            if (request.POST.get("isverify", -1) == -1):
                legal = False
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['_signid'] = int(random.uniform(10, 100))
    return JsonResponse(dict)

def signList(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            if (request.POST.get('act_id', 0) == 0):
                dict['error_code'] = 2 #invalid act_id
            ids = []
            for i in range(1, 10):
                ids.append({'id':int(random.uniform(1, 100)), 'name':'sign test'});
            dict['ids'] = ids
    return JsonResponse(dict)

def signed(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', 0) == 0):
                legal = False #invalid act_id
            if (request.POST.get('sign_id', 0) == 0):
                legal = False #invalid sign_id
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['_signid'] = request.POST.get('sign_id', 0)
                dict['signed'] = bool(int(random.uniform(0,2)))
    return JsonResponse(dict)

def msigned(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', 0) == 0):
                legal = False #invalid act_id
            if (request.POST.get('sign_id', 0) == 0):
                legal = False #invalid sign_id
            if (request.POST.get('user_id', 0) == 0):
                legal = False #invalid sign_id
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['_userid'] = request.POST.get('user_id', 0)
                dict['signed'] = bool(int(random.uniform(0,2)))
                dict['msg'] = "I signed yeah~"
    return JsonResponse(dict)

def signInfo(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', 0) == 0):
                legal = False #invalid act_id
            if (request.POST.get('sign_id', 0) == 0):
                legal = False #invalid sign_id
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['_id'] = int(request.POST.get('sign_id', 0))
                dict['name'] = 'test_sign'
                dict['timeL'] = '2016.6.1 10:45:34'
                dict['timeR'] = '2016.6.1 10:50:34'
                dict['command'] = '2333'
                dict['isface'] = bool(int(request.POST.get('sign_id', 0)) & 1)
                dict['isverify'] = bool(int(random.uniform(0,2)))
    return JsonResponse(dict)


def createVote(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            isChoose = False
            
            legal = True
            if (request.POST.get("act_id", -1) == -1):
                legal = False
            if (request.POST.get("sign_id", -1) == -1):
                legal = False
            if (request.POST.get("name", -1) == -1):
                legal = False
            if (request.POST.get("timeL", -1) == -1):
                legal = False
            if (request.POST.get("timeR", -1) == -1):
                legal = False
            if (request.POST.get("caption", -1) == -1):
                legal = False
            if (request.POST.get("ischoose", -1) == -1):
                legal = False
            else:
                isChoose = request.POST.get("ischoose", False)
            if (isChoose):
                if (request.POST.get("chooselist", -1) == -1):
                    legal = False
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['_voteid'] = int(random.uniform(10, 100))
    return JsonResponse(dict)

def voteList(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', -1) == -1):
                legal = False
            if (request.POST.get('sign_id', -1) == -1):
                legal = False
            dict['ids'] = []
            for i in range(0, 10):
                dict['ids'].append(int(random.uniform(0, 100)))
    return JsonResponse(dict)

def voteInfo(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', -1) == -1):
                legal = False
            if (request.POST.get('sign_id', -1) == -1):
                legal = False
            if (request.POST.get('vote_id', -1) == -1):
                legal = False
            dict['_id'] = request.POST.get('vote_id', -1)
            dict['name'] = "Vote for Test"
            dict['timeL'] = "2016.6.1 12:00:00"
            dict['timeR'] = "2016.6.1 13:00:00"
            dict['caption'] = "Which character do you like?"
            dict['ischoose'] = (random.uniform(0, 2) > 1)
            if (dict['ischoose']):
                dict['chooselist'] = ['A', 'B', 'C', 'D']
    return JsonResponse(dict)

def voteStat(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', -1) == -1):
                legal = False
            if (request.POST.get('sign_id', -1) == -1):
                legal = False
            if (request.POST.get('vote_id', -1) == -1):
                legal = False
            dict['timestat'] = int(random.uniform(0, 3))
            dict['stat'] = []
            dict['stat'].append({'choose': 'A', 'count': int(random.uniform(0, 100))})
            dict['stat'].append({'choose': 'B', 'count': int(random.uniform(0, 100))})
            dict['stat'].append({'choose': 'C', 'count': int(random.uniform(0, 100))})
            dict['stat'].append({'choose': 'D', 'count': int(random.uniform(0, 100))})
    return JsonResponse(dict)

def signurl(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', -1) == -1):
                legal = False
            if (request.POST.get('sign_id', -1) == -1):
                legal = False
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['qrcodeurl'] = '/media/qrcode/example.png'
                dict['url'] = '/interact/sign?code=CCOOXXDDEE'
    return JsonResponse(dict)
                
def voteurl(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if (request.POST.get('act_id', -1) == -1):
                legal = False
            if (request.POST.get('sign_id', -1) == -1):
                legal = False
            if (request.POST.get('vote_id', -1) == -1):
                legal = False
            if (not legal):
                dict['error_code'] = 2
            else:
                dict['qrcodeurl'] = '/media/qrcode/example.png'
                dict['url'] = '/interact/vote?code=CCOOXXDDEE'
    return JsonResponse(dict)

def signTimeVerify(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('code', -1) == -1):
            dict['error_code'] = 1 #no code received
        else:
            if (request.POST.get('code', -1) != "CCOOXXDDEE"):
                dict['error_code'] = 2 #invalid code
            else:
                dict['name'] = "Test Sign";
                dict['isFace'] = bool(int(random.uniform(0,2)))
                dict['isVerify'] = bool(int(random.uniform(0,2)))
    return JsonResponse(dict)

def sign(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            legal = True
            if not (request.POST.get('command', -1) == "6666"):
                legal = False
            if (request.POST.get('photo', -1) == -1):
                legal = False
            if (request.POST.get('msg', -1) == -1):
                legal = False
            if (not legal):
                dict['error_code'] = 2;
    return JsonResponse(dict)

def voteTimeVerify(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', -1) != testToken):
            dict['error_code'] = 1 
        else:
            if (request.POST.get('code', -1) != "CCOOXXDDEE"):
                dict['error_code'] = 2 #invalid code
            else:
                dict['name'] = "Test Sign";
                dict['ischoose'] = bool(int(random.uniform(0,2)))
                dict['caption'] = "Which character do you like?"
                dict['ischoose'] = (random.uniform(0, 2) > 1)
                if (dict['ischoose']):
                    dict['chooselist'] = ['A', 'B', 'C', 'D']
    return JsonResponse(dict)

def vote(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201
    else:
        dict['error_code'] = 200
        if (request.POST.get('access_token', 0) != testToken):
            dict['error_code'] = 1
        else:
            if (request.POST.get('msg', -1) == -1):
                dict['error_code'] = 2 #lack msg
    return JsonResponse(dict)

                