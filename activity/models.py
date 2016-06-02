from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length = 255)


class Activity(models.Model):
	name = models.CharField(max_length = 255)
	tags = models.ManyToManyField(Tag, related_name='activities')
	description = models.TextField(default='')
	users = models.ManyToManyField(User, related_name='activities')
	hold_users = models.ManyToManyField(User, related_name='activities_held')
	signed_users = models.ManyToManyField(User, related_name='activities_signed')
	managers = models.ManyToManyField(User, related_name='activities_managed')
	waiting_users = models.ManyToManyField(User, related_name='activities_waiting')
	ispublic = models.BooleanField(default=False)
	isverify = models.BooleanField(default=True)


class Comment(models.Model):
	text = models.TextField(default='')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='comments')
	added_time = models.DateTimeField(auto_now_add=True)


class Notice(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField(default='')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notices')
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='notices')
	added_time = models.DateTimeField(auto_now_add=True)


class UserInfoForActivity(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userinfoforactivity')
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='userinfoforactivity')