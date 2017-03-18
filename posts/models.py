from __future__ import unicode_literals

from django.db import models
from userprofiles.models import UserProfile
# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='post')
    movie_title = models.CharField(max_length=200)
    # IMDB id
    movie_id = models.CharField(max_length=20)
    caption = models.CharField(max_length=200, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.movie_title

    def __str__(self):
        return self.movie_title
