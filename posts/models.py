from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
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

    def like(self, username, r):
        print(self.movie_title)
        l = Like(rating=r)
        l.post = self
        l.likedby = UserProfile.objects.get(user__username=username)
        l.save()


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes')
    likedby = models.ForeignKey(UserProfile, related_name='all_likes')
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __unicode__(self):
        return self.likedby.user.username

    def __str__(self):
        return self.likedby.user.username
