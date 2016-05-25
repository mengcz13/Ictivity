from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from Ictuser.models import UserProfile
from activity.models import Tag, Comment, Activity
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
	activity = Activity.objects.get(id=request.POST['_id'])
	if activity is not None:
		jresp = {
		'_id': activity.id,
		'name': activity.name,
		'tags': [{'name': tag.name} for tag in activity.tags.all()],
		'description': activity.description
		}
		return JsonResponse(jresp)
	else:
		return JsonResponse({'error_code': 1})


@ensure_csrf_cookie
@login_required
def activity_holdlist(request):
	jsonresp = {
	'error_code': 200,
	'_ids': [{'_id': act.id} for act in request.user.activities_managed.all()]
	}
	return JsonResponse(jsonresp)


@ensure_csrf_cookie
@login_required
def activity_joinlist(request):
	jsonresp = {
	'error_code': 200,
	'_ids': [{'_id': act.id} for act in request.user.activities.all()]
	}
	return JsonResponse(jsonresp)