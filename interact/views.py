from django.http import HttpResponse, HttpResponseRedirect
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
from django.utils.timezone import utc, localtime
import ictivity.facepp as facepp
from ictivity.settings import FACEPP_API_KEY, FACEPP_API_SECRET, FACEPP_GROUP_NAME, FACEPP_API_URL, BASE_DIR, ROUTE_URL
import os

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
			'ids': [ {'id': sign.id, 'name': sign.name} for sign in activity.signs.all() ],
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
		if (request.POST['sign_id'] == '0'):
			return JsonResponse({
				'_userid': request.POST['user_id'],
				'signed': True,
				'msg': 'aaa',
				'error_code': 200
				})
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
			'timeL': localtime(sign.timeL),
			'timeR': localtime(sign.timeR),
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
		returnedurl = '%s/interact/sign?code=%s' % (ROUTE_URL, str(signid.id))
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
	try:
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
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
#@login_required
@require_POST
def interact_sign(request):
	try:
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/user/login')
		signid = Sign.objects.get(id=request.session['code'])
		if (signid.isface):
			if (signid.command == request.POST['command']):
				usernewphoto = UserPhoto(user=request.user, image=request.FILES['photo'])
				usernewphoto.save()
				faceapi = facepp.API(FACEPP_API_KEY, FACEPP_API_SECRET)
				res = faceapi.recognition.identify(group_name=FACEPP_GROUP_NAME, img=facepp.File(os.path.join(BASE_DIR, usernewphoto.image.url[1:])))
				usernewphoto.delete()
				if (res['face'][0]['candidate'][0]['person_name'] == request.user.username):
					newsu = SignedUser(user=request.user, msg=request.POST['msg'], sign=signid)
					newsu.save()
					return JsonResponse({'error_code': 200})
				else:
					return JsonResponse({'error_code': 1})
			else:
				return JsonResponse({'error_code': 1})
		else:
			if (signid.command == request.POST['command']):
				newsu = SignedUser(user=request.user, msg=request.POST['msg'], sign=signid)
				newsu.save()
				return JsonResponse({'error_code': 200})
			else:
				return JsonResponse({'error_code': 1})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_createVote(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		sign = Sign.objects.get(id=request.POST['sign_id'])
		newvote = Vote(sign=sign, name=request.POST['name'], timeL=request.POST['timeL'], timeR=request.POST['timeR'], caption=request.POST['caption'], ischoose=(request.POST['ischoose']=='true'))
		newvote.save()
		chooselist = request.POST['chooselist'].split(',')
		for ci in chooselist:
			newci = VoteItem(vote = newvote, name = ci, num = 0)
			newci.save()
		return JsonResponse({'_voteid': newvote.id, 'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_voteList(request):
	try:
		sign = Sign.objects.get(id=request.POST['sign_id'])
		return JsonResponse({
			'ids': [vote.id for vote in sign.votes.all()],
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_voteInfo(request):
	try:
		vote = Vote.objects.get(id=request.POST['vote_id'])
		chooselist = []
		if vote.ischoose:
			chooselist = [voteitem.name for voteitem in vote.voteitems.all()]
		return JsonResponse({
			'_id': vote.id,
			'name': vote.name,
			'timeL': vote.timeL,
			'timeR': vote.timeR,
			'caption': vote.caption,
			'ischoose': vote.ischoose,
			'chooselist': chooselist,
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_voteStat(request):
	try:
		vote = Vote.objects.get(id=request.POST['vote_id'])
		dt = timezone.now()
		timestat = 1
		if dt < vote.timeL:
			timestat = 0
		elif dt > vote.timeR:
			timestat = 2
		stat = [{'choose': voteitem.name, 'count': voteitem.num} for voteitem in vote.voteitems.all()]
		return JsonResponse({
			'timestat': timestat,
			'stat': stat,
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_voteurl(request):
	try:
		vote = Vote.objects.get(id=request.POST['vote_id'])
		returnedurl = '%s/interact/vote?code=%s' % (ROUTE_URL, str(vote.id))
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
def interact_voteTimeVerify(request):
	try:
		vote = Vote.objects.get(id=request.POST['code'])
		dt = timezone.now()
		if (dt >= vote.timeL and dt <= vote.timeR):
			request.session['code'] = request.POST['code']
			return JsonResponse({
				'error_code': 200,
				'name': vote.name,
				'caption': vote.caption,
				'ischoose': vote.ischoose,
				'chooselist': [voteitem.name for voteitem in vote.voteitems.all()]
				})
		else:
			return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def interact_vote(request):
	try:
		vote = Vote.objects.get(id=request.session['code'])
		voteitem = vote.voteitems.get(name=request.POST['msg'])
		voteitem.num = voteitem.num + 1
		voteitem.save()
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})
