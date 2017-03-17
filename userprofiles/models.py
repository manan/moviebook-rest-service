from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.conf import settings

# Create your models here.


def upload_location(instance, filename):
    return 'profilepicture_%s.jpg' % instance.user


class UserProfile(models.Model):
    GENDER_CHOICES = (
                      ('M', 'Male'),
                      ('F', 'Female'),
                      ('U', 'Unspecified')
                      )
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    # TODO: profile_picture is a non-null because default, change it later
    profile_picture = models.FileField(upload_to=upload_location, default="default-5.jpg", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False,
                                        blank=True, null=True)
    blocked = models.ManyToManyField('self', related_name='blockedby', symmetrical=False,
                                     blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def is_following(self, username=False, upid=False):
        if username:
            return self.followings.filter(user__username=username).exists()
        elif upid:
            return self.followings.filter(pk=upid).exists()
        else:
            return False

    def is_followed_by(self, username=False, upid=False):
        if username:
            return self.followers.filter(user__username=username).exists()
        elif upid:
            return self.followers.filter(pk=upid).exists()
        else:
            return False

    def is_blocked(self, username=False, upid=False):
        if username:
            return self.blocked.filter(user__username=username).exists()
        elif upid:
            return self.blocked.filter(pk=upid).exists()
        else:
            return False

    def is_blocked_by(self, username=False, upid=False):
        if username:
            return self.blockedby.filter(user__username=username).exists()
        elif upid:
            return self.blockedby.filter(pk=upid).exists()
        else:
            return False
    
    def block(self, username=False, upid=False):
        if username:
            if self.is_blocked(username=username):
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
            if self.is_blocked(upid=upid):
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
            if self.is_blocked(username=username):
                other = self.blocked.get(user__username=username)
                self.blocked.remove(other)
                self.save()
                other.save()
                return True
            else:
                return False
        elif upid:
            if self.is_blocked(upid=upid):
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
            if self.is_following(username) or self.is_blocked(username) or self.is_blocked_by(username):
                return False
            else:
                other = UserProfile.objects.get(user__username=username)
        elif upid:
            if self.is_following(upid=upid) or self.is_blocked(upid=upid) or self.is_blocked_by(upid=upid):
                return False
            else:
                other = UserProfile.objects.get(pk=upid)
        else:
            return False
        self.followings.add(other)
        other.save()
        self.save()
        return True

    def unfollow(self, username=False, upid=False):
        if username:
            if self.is_following(username):
                other = self.followings.get(user__username=username)
            else:
                return False
        elif upid:
            if self.is_following(upid=upid):
                other = self.followings.get(pk=upid)
            else:
                return False
        else:
            return False
        self.followings.remove(other)
        other.save()
        self.save()
        return True

    def remove_follower(self, username=False, upid=False):
        if username:
            if self.is_followed_by(username=username):
                other = self.followers.get(user__username=username)
            else:
                return False
        elif upid:
            if self.is_followed_by(upid=upid):
                other = self.followers.get(pk=upid)
            else:
                return False
        else:
            return False
        other.followings.remove(self)
        other.save()
        self.save()
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

