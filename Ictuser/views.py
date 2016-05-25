from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from Ictuser.models import UserProfile
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

# Create your views here.
@ensure_csrf_cookie
@require_POST
def Ictuser_register(request):
	data = request.POST
	if User.objects.filter(username=data['username']).exists():
		return JsonResponse({'error_code': 1})
	user = User.objects.create_user(data['username'], data['email'], data['password'])
	userprofile = UserProfile.objects.create(user=user, location=data['location'], birthday=data['birthday'], nickname='', face_id='', age=0)
	return JsonResponse({'error_code': 0, '_id': user.id})


@ensure_csrf_cookie
def Ictuser_login(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			return JsonResponse({'error_code': 200, '_id': request.user.id})
		lf = LoginForm()
		return render_to_response('loginform.html', {'form': lf}, context_instance=RequestContext(request))
	elif request.method == 'POST':
		un = request.POST['username']
		pw = request.POST['password']
		user = authenticate(username=un, password=pw)
		if user is not None:
			if user.is_active:
				login(request, user)
				return JsonResponse({'error_code': 200, '_id': user.id})
			else:
				return JsonResponse({'error_code': 3})
		elif not User.objects.filter(username=request.POST['username']).exists():
			return JsonResponse({'error_code': 1})
		else:
			return JsonResponse({'error_code': 2})


@ensure_csrf_cookie
def Ictuser_logout(request):
	logout(request)
	return JsonResponse({'error_code': 200})


@login_required
@ensure_csrf_cookie
def Ictuser_userinfo(request):
	return JsonResponse({
		'error_code': 200,
		'username': request.user.username,
		'emali': request.user.email,
		'location': request.user.userprofile.location,
		'birthday': request.user.userprofile.birthday
		})