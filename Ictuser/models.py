from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length = 255, default='')
    age = models.SmallIntegerField(default=0)
    birthday = models.DateField(default='1970-01-01')
    location = models.CharField(max_length = 255, default='')
    face_id = models.TextField(default='')