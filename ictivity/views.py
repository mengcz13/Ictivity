# -*- coding: utf-8 -*-
# @Author: mengcz13
# @Date:   2016-06-03 10:05:45
# @Last Modified by:   mengcz13
# @Last Modified time: 2016-06-03 19:08:27
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from Ictuser.models import UserProfile
from activity.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods, require_POST

@ensure_csrf_cookie
@require_POST
def search(request):
	try:
		wd = request.POST['wd']
		idlist = [act.id for act in Activity.objects.filter(name__contains=wd) if act.ispublic]
		return JsonResponse({
			'error_code': 200,
			'ids': idlist
			})
	except:
		return JsonResponse({'error_code': 1})