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
def interact_sign(request):
	user = request.user
	activity = Activity.objects.get(id=request.POST['activity_id'])
	if activity is not None:
		activity.signed_users.add(user)
		return JsonResponse({'error_code': 200})
	else:
		return JsonResponse({'error_code': 1})