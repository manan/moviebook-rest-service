from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Follow(models.Model):
    following = models.ForeignKey(User, related_name = "who_follows")
    follower = models.ForeignKey(User, related_name = "who_is_followed")
    follow_time = models.DateTimeField(auto_now = True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank = True, null = True)
    birth_date = models.DateField(blank = True, null = True)

class Post(models.Model):
    owner = models.ForeignKey(User, related_name = 'posts')
    movie_title = models.CharField(max_length = 200)
    movie_id = models.CharField(max_length = 20)
