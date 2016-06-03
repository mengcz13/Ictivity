from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from Ictuser.models import UserProfile
from activity.models import *

# Create your models here.


class Sign(models.Model):
	name = models.CharField(max_length = 255)
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='signs')
	timeL = models.DateTimeField()
	timeR = models.DateTimeField()
	users = models.ManyToManyField(User, related_name='signs')