from django.shortcuts import render
from rest_framework import generics, permissions

from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile, Post
from .serializers import UserProfileReadSerializer, UserProfileWriteSerializer
from .serializers import RegistrationSerializer, PostSerializer
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from datetime import datetime
from datetime import timedelta

# Create your views here.

class NewsFeed(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        userp = User.objects.get(pk = self.kwargs['userid'].strip()).profile
        people = userp.followings.all()
        acc = []
        for person in people:
            for post in person.post.filter(upload_date__gte=datetime.now() - timedelta(days=2)):
                acc.append(post)
        acc.sort(key=lambda x: x.upload_date, reverse=True)
        return acc

class DeletePost(generics.DestroyAPIView):
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'
    permission_classes = [
        permissions.AllowAny
    ]

class UpdatePost(generics.UpdateAPIView):
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'
    permission_classes = [
        permissions.AllowAny
    ]

@csrf_exempt
def AddFollowerPUT(request):
    if request.method != 'PUT':
        content = {'Only PUT requests are allowed'}
        return HttpResponse(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not (len(request.body.replace(' ', '').split(',')) < 2):
        username1 = request.body.replace(' ', '').replace('{','').split(',')[0]
        username2 = request.body.replace(' ', '').replace('}','').split(',')[1]
        if not User.objects.get(username=username1).profile.followers.filter(user__username=username2).exists():
            User.objects.get(username=username1).profile.followings.add(User.objects.get(username=username2).profile)
            User.objects.get(username=username2).profile.followers.add(User.objects.get(username=username1).profile)
            return HttpResponse({'Done!'}, status=status.HTTP_200_OK)
        else:
            return HttpResponse({'Failed!'}, staus=status.HTTP_412_PRECONDITION_FAILED)
    else:
        return HttpResponse('Failed!', staus=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def RemoveFollowerPUT(request):
    if request.method != 'PUT':
        content = {'Only PUT requests are allowed'}
    if not (len(request.body.replace(' ', '').split(',')) < 2):
        username1 = request.body.replace(' ', '').replace('{','').split(',')[0]
        username2 = request.body.replace(' ', '').replace('}','').split(',')[1]
        if User.objects.get(username=username1).profile.followings.filter(user__username=username2).exists():
            User.objects.get(username=username1).profile.followings.remove(User.objects.get(username=username2).profile)
            User.objects.get(username=username2).profile.followers.remove(User.objects.get(username=username1).profile)
            return HttpResponse({'Done!'}, status=status.HTTP_200_OK)
        else:
            return HttpResponse({'Failed!'}, staus=status.HTTP_412_PRECONDITION_FAILED)
    else:
        return HttpResponse('Failed!', staus=status.HTTP_400_BAD_REQUEST)
    
class PostsOfUser(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        id = self.kwargs['id'].strip()
        user = User.objects.get(pk=int(id))
        return user.profile.post.all()


class PostsByIDs(generics.ListAPIView):
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


class ProfilesByIDs(generics.ListAPIView):
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


class SearchProfiles(generics.ListAPIView):
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


class ProfileByUsername(generics.ListAPIView):
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
