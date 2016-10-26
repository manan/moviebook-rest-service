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
    # relationships = models.ManyToManyField(Follow, symmetrical=False, related_name='related_to',
                                           # null = True, blank = True)
