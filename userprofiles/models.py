
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import os
from django.conf import settings

# Create your models here.

def upload_location_rm_dup(instance, filename):
    imgname =  '%s.jpg' %(instance.user)
    path = os.path.join(settings.MEDIA_ROOT, imgname)
    if os.path.exists(path):
        os.remove(path)
    return imgname

def upload_location(instance, filename):
    return '%s.jpg' %(instance.user)

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name = 'profile')
    bio = models.TextField(blank = True, null = True)
    birth_date = models.DateField(blank = True, null = True)
    profile_picture = models.FileField(upload_to = upload_location, blank = True, null = True) 
    followings = models.ManyToManyField('self', related_name = 'followers', symmetrical=False,
                                        blank = True, null = True)
    blocked = models.ManyToManyField('self', related_name = 'blockedby', symmetrical=False,
                                     blank = True, null = True)
    following_count = models.IntegerField(default=0, blank = True, null = True)
    follower_count = models.IntegerField(default=0, blank = True, null = True)

    def __unicode__(self):
        return self.user.username

    def isFollowing(self, username=False, upid=False):
        if username:
            return self.followings.filter(user__username=username).exists()
        elif upid:
            return self.followings.filter(pk=upid).exists()
        else:
            return False

    def isFollowedBy(self, username=False, upid=False):
        if username:
            return self.followers.filter(user__username=username).exists()
        elif upid:
            return self.followers.filter(pk=upid).exists()
        else:
            return False

    def isBlocked(self, username=False, upid=False):
        if username:
            return self.blocked.filter(user__username=username).exists()
        elif upid:
            return self.blocked.filter(pk=upid).exists()
        else:
            return False

    def isBlockedBy(self, username=False, upid=False):
        if username:
            return self.blockedby.filter(user__username=username).exists()
        elif upid:
            return self.blockedby.filter(pk=upid).exists()
        else:
            return False
    
    def block(self, username=False, upid=False):
        if username:
            if self.isBlocked(username=username):
                return False
            else:
                other = User.objects.get(username=username).profile
                self.blocked.add(other)
                self.unfollow(username)
                other.unfollow(self.user.username)
                self.save()
                other.save()
                return True
        elif upid:
            if self.isBlocked(upid=upid):
                return False
            else:
                other = UserProfile.objects.get(pk=upid)
                self.blocked.add(other)
                self.unfollow(upid=upid)
                other.unfollow(self.user.username)
                self.save()
                other.save()
                return True
        else:
            return False

    def unblock(self, username=False, upid=False):
        if username:
            if self.isBlocked(username=username):
                other = self.blocked.get(user__username=username)
                self.blocked.remove(other)
                self.save()
                other.save()
                return True
            else:
                return False
        elif upid:
            if self.isBlocked(upid=upid):
                other = self.blocked.get(pk=upid)
                self.blocked.remove(other)
                self.save()
                other.save()
                return True
            else:
                return False;
        else:
            return False

    def follow(self, username=False, upid=False):
        if username:
            if self.isFollowing(username) or self.isBlocked(username) or self.isBlockedBy(username):
                return False
            else:
                other = UserProfile.objects.get(user__username=username)
        elif upid:
            if self.isFollowing(upid=upid) or self.isBlocked(upid=upid) or self.isBlockedBy(upid=upid):
                return False
            else:
                other = UserProfile.objects.get(pk=upid)
        else:
            return False
        self.followings.add(other)
        self.following_count = self.followings.all().count()
        self.follower_count = self.followers.all().count()
        other.following_count = other.followings.all().count()
        other.follower_count = other.followers.all().count()
        other.save()
        self.save()
        return True

    def unfollow(self, username=False, upid=False):
        if username:
            if self.isFollowing(username):
                other = self.followings.get(user__username=username)
            else:
                return False
        elif upid:
            if self.isFollowing(upid=upid):
                other = self.followings.get(pk=upid)
            else:
                return False
        else:
            return False
        self.followings.remove(other)
        self.following_count = self.followings.all().count()
        self.follower_count = self.followers.all().count()
        other.following_count = other.followings.all().count()
        other.follower_count = other.followers.all().count()
        other.save()
        self.save()
        return True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    
class Post(models.Model):
    owner = models.ForeignKey(UserProfile, related_name = 'post')
    movie_title = models.CharField(max_length = 200)
    movie_id = models.CharField(max_length = 20)
    caption = models.CharField(max_length = 200, blank = True, null = True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.movie_title
