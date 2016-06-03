from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from Ictuser.models import *
from activity.models import *

# Create your models here.


class Sign(models.Model):
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='signs')
	name = models.CharField(max_length = 255)
	timeL = models.DateTimeField()
	timeR = models.DateTimeField()
	command = models.CharField(max_length = 255)
	isface = models.BooleanField(default=False)
	isverify = models.BooleanField(default=False)


class SignedUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signedrecord')
	msg = models.CharField(max_length = 255)
	sign = models.ForeignKey(Sign, on_delete=models.CASCADE, related_name='signedusers')