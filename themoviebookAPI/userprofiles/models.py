from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, unique=True, related_name = 'user')
    bio = models.TextField(blank = True, null = True)
    birth_date = models.DateField(blank = True, null = True)
    follows = models.ManyToManyField("self", related_name = 'following', symmetrical=False)

class Post(models.Model):
    owner = models.ForeignKey('auth.User', related_name = 'posts')
    movie_title = models.CharField(max_length = 200)
    movie_id = models.CharField(max_length = 20)
