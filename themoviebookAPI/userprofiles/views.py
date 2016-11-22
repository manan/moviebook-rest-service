from django.shortcuts import render
from rest_framework import generics, permissions

from .models import UserProfile, Post
from .serializers import UserProfileSerializer, RegistrationSerializer, PostSerializer
from django.contrib.auth.models import User

from django.db.models import Q

# Create your views here.

class PostByKey(generics.ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        ids = self.kwargs['id'].split(',')
        print ids
        ids = [int(every) for every in ids]
        ret = set()
        for everyid in ids:
            ret.add(Post.objects.get(pk=everyid))
        return ret

class ProfileSearch(generics.ListCreateAPIView):
    model = UserProfile
    serializer_class = UserProfileSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        name = self.kwargs['name']
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
    serializer_class = UserProfileSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        uname = self.kwargs['username']
        ret = set()
        for every in User.objects.filter(username__contains = uname):
            ret.add(every.profile)
        return ret

class UserList(generics.ListCreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class PostList(generics.ListCreateAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

class ProfileList(generics.ListCreateAPIView):
    model = UserProfile
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [
        permissions.AllowAny
    ]
