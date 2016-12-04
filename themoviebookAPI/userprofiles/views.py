from django.shortcuts import render
from rest_framework import generics, permissions

from django.http import HttpResponseRedirect, HttpResponse

from .models import UserProfile, Post
from .serializers import UserProfileReadSerializer, UserProfileWriteSerializer
from .serializers import RegistrationSerializer, PostSerializer
from django.contrib.auth.models import User

from django.db.models import Q

# Create your views here.
    
class PostsOfUser(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        id = self.kwargs['id'].strip()
        user = User.objects.get(pk=int(id))
        return user.profile.post.all()


class PostsByIDs(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        ids = self.kwargs['ids'].replace(' ', '').split(',')
        ids = [int(every) for every in ids]
        ret = set()
        for everyid in ids:
            try:
                ret.add(Post.objects.get(pk=everyid))
            except (Post.DoesNotExist):
                pass
        return ret


class ProfilesByIDs(generics.ListCreateAPIView):
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        ids = self.kwargs['ids'].replace(' ', '').split(',')
        ids = [int(every) for every in ids]
        ret = set()
        for everyid in ids:
            try:
                ret.add(UserProfile.objects.get(pk=everyid))
            except (UserProfile.DoesNotExist):
                pass
        return ret


class SearchProfiles(generics.ListCreateAPIView):
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        name = self.kwargs['name'].strip()
        ret = set()
        if (len(name.split(' ')) == 1):
            for every in User.objects.filter(Q(first_name__icontains = name)
                                             | Q(last_name__icontains = name)
                                             | Q(username__icontains = name)):
                ret.add(every.profile)
        elif (len(name.split(' ')) >= 2):
            fname = name.split(' ')[0]
            lname = name.split(' ')[1]
            for every in User.objects.filter(Q(first_name__contains = fname) |
                                             Q(last_name__contains = lname) |
                                             Q(first_name__contains = lname) |
                                             Q(last_name__contains = fname) |
                                             Q(username__contains = fname) |
                                             Q(username__contains = lname)):
                ret.add(every.profile)
        return ret


class ProfileByUsername(generics.ListCreateAPIView):
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        uname = self.kwargs['username']
        ret = set()
        try:
            user = User.objects.get(username = uname)
            ret.add(user.profile)
        except (User.DoesNotExist):
            print ("Couldn't find a match")
        return ret


class UserList(generics.ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_create(self, serializer):
        print 'UserList.perform_create called'
        serializer.save()

class PostList(generics.ListCreateAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_create(self, serializer):
        print 'PostList.perform_create called'
        serializer.save()
    
class ProfileList(generics.ListCreateAPIView):
    model = UserProfile
    queryset = UserProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_create(self, serializer):
        print 'ProfileList.perform_create called'
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == ('POST' or 'PUT' or 'PATCH'):
            return UserProfileWriteSerializer
        else:
            return UserProfileReadSerializer
