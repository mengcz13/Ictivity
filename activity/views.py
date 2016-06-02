from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from Ictuser.models import UserProfile
from activity.models import Tag, Comment, Activity, Notice
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
	activity = Activity.objects.create(name=data['name'], description=data['description'])
	for tagn in data['tag'].split():
		tag = Tag.objects.create(name=tagn)
		activity.tags.add(tag)
	activity.users.add(request.user)
	activity.hold_users.add(request.user)
	activity.managers.add(request.user)
	return JsonResponse({'error_code': 200, '_id': activity.id})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_info(request):
	activity = Activity.objects.get(id=request.POST['id'])
	if activity is not None:
		if not activity.ispublic:
			if not activity.users.filter(id=request.user.id).exists():
				return JsonResponse({'error_code': 1})
		jresp = {
		'id': activity.id,
		'name': activity.name,
		'tags': [{'name': tag.name} for tag in activity.tags.all()],
		'description': activity.description,
		'count': activity.users.count()
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
	'ids': [{'id': act.id} for act in request.user.activities_managed.all()]
	}
	return JsonResponse(jsonresp)


@ensure_csrf_cookie
@login_required
@require_POST
def activity_joinlist(request):
	jsonresp = {
	'error_code': 200,
	'ids': [{'id': act.id} for act in request.user.activities.all()]
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
		'id': activity.id,
		'name': activity.name,
		'tags': [{'name': tag.name} for tag in activity.tags.all()],
		'description': activity.description,
		'count': activity.users.count()
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
		activity.tags.all().delete()
		activity.update(description=request.POST['description'], ispublic=request.POST['ispublic'], isverify=request.POST['isverify'])
		for tagn in data['tag'].split():
			tag = Tag.objects.create(name=tagn)
			activity.tags.add(tag)
		return JsonResponse({'error_code': 200})
	else:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_role(request):
	activity = Activity.objects.get(id=request.POST['id'])
	if activity is not None:
		if activity.managers.filter(id=request.user.id).exists():
			return JsonResponse({'role': 2, 'error_code': 200})
		elif activity.users.filter(id=request.user.id).exists():
			return JsonResponse({'role': 1, 'error_code': 200})
		else:
			return JsonResponse({'role': 0, 'error_code': 200})
	else:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_join(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		activity.waiting_users.add(request.user)
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_notices(request):
	try:
		activity = Activity.objects.get(id=request.POST['id'])
		if not activity.users.filter(id=request.user.id).exists():
			return JsonResponse({'error_code': 1})
		notices = activity.notices.ordered_by('-added_time').all()
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
		if not activity.users.filter(id=request.user.id).exists():
			return JsonResponse({'error_code': 1})
		comments = activity.comments.ordered_by('-added_time').all()
		return JsonResponse({
			'comments': [{'text': comm.text, 'nickname': comm.user.username, 'time': comm.added_time} for comm in comments],
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
		if not activity.users.filter(id=request.user.id).exists():
			return JsonResponse({'error_code': 1})
		return JsonResponse({
			'members': [{'nickname': user.username, 'ismanager': activity.users.filter(id=user.id).exists()} for user in activity.users.all()],
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
		if not activity.users.filter(id=request.user.id).exists():
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
		if not activity.managers.filter(id=request.user.id).exists():
			return JsonResponse({'error_code': 1})
		Notice.objects.create(title=request.POST['title'], text=request.POST['notice'], author=request.user, activity=activity)
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
@require_POST
def activity_verifyList(request):
	pass


@ensure_csrf_cookie
@login_required
@require_POST
def activity_verifyReject(request):
	pass


@ensure_csrf_cookie
@login_required
@require_POST
def activity_verifyPass(request):
	pass
		