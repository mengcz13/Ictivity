from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from Ictuser.models import *
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST
import ictivity.facepp as facepp
from ictivity.settings import FACEPP_API_KEY, FACEPP_API_SECRET, FACEPP_GROUP_NAME, FACEPP_API_URL, BASE_DIR
import requests
import os
from django.utils.timezone import utc, localtime

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
	nickname = data['username']
	userprofile = UserProfile.objects.create(user=user, location=data['location'], birthday=data['birthday'], nickname=nickname, face_id='', age=0)
	return JsonResponse({'error_code': 200, '_id': user.id})


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
@require_POST
def Ictuser_logout(request):
	logout(request)
	return JsonResponse({'error_code': 200})


@login_required
@ensure_csrf_cookie
@require_POST
def Ictuser_userinfo(request):
	return JsonResponse({
		'error_code': 200,
		'username': request.user.username,
		'email': request.user.email,
		'location': request.user.userprofile.location,
		'birthday': request.user.userprofile.birthday
		})


@login_required
@ensure_csrf_cookie
@require_POST
def Ictuser_changeinfo(request):
	try:
		request.user.email = request.POST['email']
		request.user.userprofile.location = request.POST['location']
		request.user.userprofile.birthday = request.POST['birthday']
		request.user.userprofile.save()
		request.user.save()
		return JsonResponse({'error_code': 200})
	except:
		return JsonResponse({'error_code': 1})


@login_required
@ensure_csrf_cookie
@require_POST
def Ictuser_changepwd(request):
	user = authenticate(username=request.user.username, password=request.POST['oldpwd'])
	if user is not None:
		user.set_password(request.POST['newpwd'])
		return JsonResponse({'error_code': 200})
	else:
		return JsonResponse({'error_code': 1})


@login_required
@ensure_csrf_cookie
@require_POST
def Ictuser_token(request):
	return JsonResponse({'error_code': 200, 'access_token': request.user.id})


@login_required
@ensure_csrf_cookie
@require_POST
def Ictuser_photos(request):
	return JsonResponse({
		'error_code': 200,
		'photos': [ { 'url': photo.image.url, 'time': localtime(photo.added_time) } for photo in request.user.photos.all() ]
		})


@login_required
@ensure_csrf_cookie
@require_POST
def Ictuser_uploadphoto(request):
	usernewphoto = UserPhoto(user=request.user, image=request.FILES['photo'])
	usernewphoto.save()
	faceapi = facepp.API(FACEPP_API_KEY, FACEPP_API_SECRET)
	if request.user.userprofile.face_id == '':
		fpppc = faceapi.person.create(person_name=request.user.username, group_name=FACEPP_GROUP_NAME)
		request.user.userprofile.face_id = fpppc['person_id']
		request.user.userprofile.save()
	print os.path.join(BASE_DIR, usernewphoto.image.url[1:])
	newface = faceapi.detection.detect(img=facepp.File(os.path.join(BASE_DIR, usernewphoto.image.url[1:])))
	try:
		faceapi.person.add_face(person_id=request.user.userprofile.face_id, face_id=newface['face'][0]['face_id'])
	except:
		pass
	faceapi.train.identify(group_name=FACEPP_GROUP_NAME)
	return JsonResponse({'error_code': 200})