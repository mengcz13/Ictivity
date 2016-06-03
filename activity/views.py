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

# Create your views here.
@ensure_csrf_cookie
@login_required
@require_POST
def activity_create(request):
	data = request.POST
	activity = Activity(name=data['name'], description=data['description'], ispublic=(request.POST['ispublic'] == 'true'), isverify=(request.POST['isverify'] == 'true'))
	activity.save()
	for tagn in data['tags'].split(','):
		try:
			tag = Tag.objects.get(name=tagn)
			activity.tags.add(tag)
		except:
			tag = Tag.objects.create(name=tagn)
			activity.tags.add(tag)
	userinfo = UserInfoForActivity(user=request.user, activity=activity, iswaitingforva=False, ispart=True, ismanager=True, isfounder=True, nicknameforact=request.user.username)
	userinfo.save()
	return JsonResponse({'error_code': 200, '_id': activity.id})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_info(request):
	activity = Activity.objects.get(id=request.POST['id'])
	if activity is not None:
		if not activity.ispublic:
			if not activity.userinfoforactivity.filter(user=request.user, ispart=True).exists():
				return JsonResponse({'error_code': 1})
		jresp = {
		'error_code': 200,
		'id': activity.id,
		'name': activity.name,
		'tags': [tag.name for tag in activity.tags.all()],
		'description': activity.description,
		'count': activity.userinfoforactivity.filter(ispart=True).count(),
		'ispublic': activity.ispublic,
		'isverify': activity.isverify
		}
		return JsonResponse(jresp)
	else:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_holdlist(request):
	jsonresp = {
	'error_code': 200,
	'ids': [{'id': act.activity.id} for act in request.user.userinfoforactivity.filter(isfounder=True)]
	}
	return JsonResponse(jsonresp)


@ensure_csrf_cookie
@login_required
@require_POST
def activity_joinlist(request):
	jsonresp = {
	'error_code': 200,
	'ids': [{'id': act.activity.id} for act in request.user.userinfoforactivity.filter(ispart=True)]
	}
	return JsonResponse(jsonresp)


@ensure_csrf_cookie
@require_POST
def activity_ginfo(request):
	activity = Activity.objects.get(id=request.POST['id'])
	if activity is not None:
		if not activity.ispublic:
			return JsonResponse({'error_code': 1})
		jresp = {
		'error_code': 200,
		'id': activity.id,
		'name': activity.name,
		'tags': [tag.name for tag in activity.tags.all()],
		'description': activity.description,
		'count': activity.userinfoforactivity.filter(ispart=True).count(),
		'ispublic': activity.ispublic,
		'isverify': activity.isverify
		}
		return JsonResponse(jresp)
	else:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_editinfo(request):
	activity = Activity.objects.get(id=request.POST['id'])
	if activity is not None:
		activity.tags.clear()
		activity.description = request.POST['description']
		activity.ispublic = (request.POST['ispublic'] == 'true')
		activity.isverify=(request.POST['isverify'] == 'true')
		activity.save()
		data = request.POST
		for tagn in data['tags'].split(','):
			try:
				tag = Tag.objects.get(name=tagn)
				activity.tags.add(tag)
			except:
				tag = Tag.objects.create(name=tagn)
				activity.tags.add(tag)
		return JsonResponse({'error_code': 200})
	else:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_role(request):
	try:
		uiforact = request.user.userinfoforactivity.get(activity=Activity.objects.get(id=request.POST['id']))
		if uiforact is None:
			return JsonResponse({'role': 0, 'error_code': 200})
		if uiforact.ismanager:
			return JsonResponse({'role': 2, 'error_code': 200})
		elif uiforact.ispart:
			return JsonResponse({'role': 1, 'error_code': 200})
		else:
			return JsonResponse({'role': 0, 'error_code': 200})
	except:
		return JsonResponse({'role': 0, 'error_code': 200})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_join(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		ui = UserInfoForActivity(user=request.user, activity=activity, nicknameforact=request.POST['nickname'], join_msg=request.POST['join_msg'])
		if not activity.isverify:
			ui.iswaitingforva = False
			ui.ispart = True
		ui.save()
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_notices(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		if not activity.userinfoforactivity.filter(user=request.user, ispart=True).exists():
			return JsonResponse({'error_code': 1})
		notices = activity.notices.all().order_by('-added_time')
		return JsonResponse({
			'notices': [{'title': note.title, 'text': note.text, 'time': note.added_time} for note in notices],
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_comments(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		if not activity.userinfoforactivity.filter(user=request.user, ispart=True).exists():
			return JsonResponse({'error_code': 1})
		comments = activity.comments.all().order_by('-added_time')
		return JsonResponse({
			'comments': [{'text': comm.text, 'nickname': activity.userinfoforactivity.get(user=comm.author).nicknameforact, 'time': comm.added_time} for comm in comments],
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_members(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		if not activity.userinfoforactivity.filter(user=request.user, ispart=True).exists():
			return JsonResponse({'error_code': 1})
		return JsonResponse({
			'members': [{'id': ui.user.id, 'nickname': ui.nicknameforact, 'ismanager': ui.ismanager} for ui in activity.userinfoforactivity.filter(ispart=True)],
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_newcomment(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		if not activity.userinfoforactivity.filter(user=request.user, ispart=True).exists():
			return JsonResponse({'error_code': 1})
		Comment.objects.create(text=request.POST['comment'], author=request.user, activity=activity)
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_newnotice(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		if not activity.userinfoforactivity.filter(user=request.user, ismanager=True).exists():
			return JsonResponse({'error_code': 1})
		Notice.objects.create(title=request.POST['title'], text=request.POST['notice'], author=request.user, activity=activity)
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_verifyList(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		if not activity.userinfoforactivity.filter(user=request.user, ismanager=True).exists():
			return JsonResponse({'error_code': 1})
		return JsonResponse({
			'list': [{'id': ui.user.id, 'msg': ui.join_msg} for ui in activity.userinfoforactivity.filter(iswaitingforva=True)],
			'error_code': 200
			})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_verifyReject(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		if not activity.userinfoforactivity.filter(user=request.user, ismanager=True).exists():
			return JsonResponse({'error_code': 1})
		ui = activity.userinfoforactivity.filter(user=User.objects.get(id=request.POST['id']))
		ui.delete()
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_verifyPass(request):
	try:
		activity = Activity.objects.get(id=request.POST['act_id'])
		if not activity.userinfoforactivity.filter(user=request.user, ismanager=True).exists():
			return JsonResponse({'error_code': 1})
		ui = activity.userinfoforactivity.get(user=User.objects.get(id=request.POST['id']))
		ui.iswaitingforva = False;
		ui.ispart = True;
		ui.save()
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})
		