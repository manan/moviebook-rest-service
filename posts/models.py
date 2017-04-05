from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from userprofiles.models import UserProfile
# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='posts')
    movie_title = models.CharField(max_length=200)
    movie_id = models.CharField(max_length=20)
    caption = models.CharField(max_length=200, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.movie_title

    def __str__(self):
        return self.movie_title

    def like(self, user_profile, r):
        l = Like(rating=r)
        l.post = self
        l.likeby = user_profile
        l.save()

    def comment(self, user_profile, co):
        c = Comment(content=co)
        c.post = self
        c.commentby = user_profile
        c.save()


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes')
    likeby = models.ForeignKey(UserProfile, related_name='all_likes')
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __unicode__(self):
        return self.likeby.user.username

    def __str__(self):
        return self.likeby.user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    commentby = models.ForeignKey(UserProfile, related_name='all_comments')
    content = models.TextField(blank=False)

    def __unicode__(self):
        return self.commentby.user.username

    def __str__(self):
        return self.commentby.user.username
