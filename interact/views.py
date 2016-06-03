from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from Ictuser.models import *
from activity.models import *
from interact.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods, require_POST
from datetime import datetime
from django.utils import timezone

# Create your views here.
@ensure_csrf_cookie
@login_required
@require_POST
def interact_createSign(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		ui = UserInfoForActivity.objects.get(user=request.user, activity=activity, ismanager=True)
		newsign = Sign(activity=activity, name=request.POST['name'], timeL=request.POST['timeL'], timeR=request.POST['timeR'], command=request.POST['command'], isface=(request.POST['isface']=='true'), isverify=(request.POST['isverify']=='true'))
		newsign.save()
		return JsonResponse({'_signid': newsign.id, 'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_signList(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		ui = UserInfoForActivity.objects.get(user=request.user, activity=activity, ispart=True)
		return JsonResponse({
			'ids': [ sign.id for sign in activity.signs.all() ],
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_msigned(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		manageri = UserInfoForActivity.objects.get(user=request.user, activity=activity, ismanager=True)
		sign = Sign.objects.get(id=request.POST['sign_id'])
		targetuser = sign.signedusers.filter(user=User.objects.get(id=request.POST['user_id']))
		if targetuser.exists():
			targetuser = targetuser[0]
			return JsonResponse({
				'_userid': targetuser.user.id,
				'signed': True,
				'msg': targetuser.msg,
				'error_code': 200
				})
		else:
			return JsonResponse({
				'_userid': request.POST['user_id'],
				'signed': False,
				'msg': '',
				'error_code': 200
				})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_signed(request):
	try:
		sign = Sign.objects.get(id=request.POST['sign_id'])
		ui = UserInfoForActivity.objects.get(user=request.user, activity=activity, ispart=True)
		targetuser = sign.signedusers.filter(user=request.user)
		if targetuser.exists():
			return JsonResponse({
				'_signid': sign.id,
				'signed': True,
				'error_code': 200
				})
		else:
			return JsonResponse({
				'_signid': sign.id,
				'signed': False,
				'error_code': 200
				})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_signinfo(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		sign = Sign.objects.get(id=request.POST['sign_id'])
		ui = UserInfoForActivity.objects.get(user=request.user, activity=activity, ismanager=True)
		return JsonResponse({
			'_id': sign.id,
			'name': sign.name,
			'timeL': sign.timeL,
			'timeR': sign.timeR,
			'command': sign.command,
			'isface': sign.isface,
			'isverify': sign.isverify,
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_signurl(request):
	try:
		signid = Sign.objects.get(id=request.POST['sign_id'])
		returnedurl = '/interact/sign?code=%s' % (str(signid.id))
		return JsonResponse({
			'qrcodeurl': 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=%s' % (returnedurl),
			'url': returnedurl,
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_signTimeVerify(request):
	#try:
		signid = Sign.objects.get(id=request.POST['code'])
		dt = timezone.now()
		print dt
		print signid.timeL
		print signid.timeR
		if (dt >= signid.timeL and dt <= signid.timeR):
			request.session['code'] = request.POST['code']
			return JsonResponse({
				'error_code': 200,
				'name': signid.name,
				'isFace': signid.isface,
				'isVerify': signid.isverify
				})
		else:
			return JsonResponse({'error_code': 1})
	#except:
		#return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_sign(request):
	try:
		signid = Sign.objects.get(id=request.session['code'])
		if (signid.command == request.POST['command']):
			newsu = SignedUser(user=request.user, msg=request.POST['msg'], sign=signid)
			newsu.save()
			return JsonResponse({'error_code': 200})
		else:
			return JsonResponse({'error_code': 1})
	except:
		return JsonResponse({'error_code': 1})