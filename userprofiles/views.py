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
from django.views.decorators.http import require_http_methods

from django.db.models import Q

from datetime import datetime
from datetime import timedelta

#### DONE
## Sign up
## Building profile
## Modify bio, birth-date, first_name, last_name, username, email
## Follow someone (works with GET, check with PATCH)
## Searching for a user

## Getting all the posts of a user for displaying his profile

## Uploading a post
## Modifying a post
## Deleting a post

## Getting posts for a newsfeed

#### TODO
## Changing password
## Blocking a user
## Change follower/following implementation

# Create your views here.

#require_http_methods(['GET'])
@csrf_exempt
def Follow(request, username1, username2):
    """
    GET request: result -> username2 follows username1

    Required Keys for GET: username1, username2

    On invalid username: 412 Precondition Failed
    On invalid method: 405 Method not allowed 
    If not formatted properly: 412 Precondition Failed
    If username2 doesn't follow username1: 412 Precondition Failed
    """

#require_http_methods(['GET'])
class PostsOfUser(generics.ListAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/posts/search/userid=<id>/
    GET request fetches all the posts of a certain user

    Required Keys for GET: <user id>

    On invalid user: []
    No ids mentioned: 404 Page not found
    """
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        id = self.kwargs['id'].strip()
        try:
            return User.objects.get(pk=int(id)).profile.post.all()
        except Exception:
            return set()

#require_http_methods(['GET'])
class PostsByIDs(generics.ListAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/posts/search/postids=<id1>,<id2>...<idn>/
    GET request fetches all the posts with the given post ids

    Required Keys for GET: at least one id

    On no match: []
    No ids mentioned: 404 Page not found
    """
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

#require_http_methods(['GET'])
class ProfilesByIDs(generics.ListAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/profiles/search/search/userids=<id1>,<id2>,..<idn>/
    GET request fetches the users with the given user ids

    Required Keys for GET: at least one id

    On no matches: []
    No ids mentioned: 404 Page not found
    """
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

#require_http_methods(['GET'])
class SearchProfiles(generics.ListAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/profiles/search/name=<name>/
    GET request fetches all the users with an approximate match

    Required Keys for GET: <name>

    On no matches: []
    """
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

#require_http_methods(['GET'])
class ProfileByUsername(generics.ListAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/profiles/search/username=<username>/
    GET request fetches the user (userprofile model) with the given username

    Required Keys for GET: <username>

    On no match: []
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        uname = self.kwargs['username']
        ret = set()
        try:
            user = User.objects.get(username=uname)
            ret.add(user.profile)
        except (User.DoesNotExist):
            print ("Couldn't find a match")
        return ret

#require_http_methods(['GET', 'POST'])
class UserList(generics.ListCreateAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/users/
    GET request fetches all the users in the db
    POST request body {"username":<>, "password":<>, "email":<>, "first_name":<>, "last_name":<>}
    adds user to the db

    Required Keys for POST: username, password, email, first_name, last_name

    On used username: {"username":["A user with that username already exists."]}
    On missing any fields: 500 Internal Server Error
    """
    model = User
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_update(self, serializer):                                                           
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])                                 
            serializer.save(password=password)                                                      
        else:
            serializer.save()

#require_http_methods(['GET', 'POST'])
class PostList(generics.ListCreateAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/posts/
    GET request fetches all the posts of the all the users in the db
    POST request body {"user":<id>, "movie_title":<bio>, "movie_id":"<imdbid>", "caption":"<cap>"}
    adds post (with owner being the user specified) to the db

    Required Keys for POST: user, movie_id

    On invalid user: {"user":["Invalid pk \"4\" - object does not exist."]}
    On missing movie_id field: {"movie_id":["This field is required."]}
    On missing owner field: {"owner":["This field is required."]}
    """
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.AllowAny
    ]

#require_http_methods(['GET', 'POST'])
class ProfileList(generics.ListCreateAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/profiles/
    GET request fetches the userprofiles of the all the users in the db
    POST request body {"user":<id>, "bio":<bio>, "birth_date":"<YYYY-MM-DD>"} adds profile to db

    Required Keys for POST: user

    On collision: {"user":["This field must be unique."]}
    On invalid user: {"user":["Invalid pk \"4\" - object does not exist."]}
    
    """
    model = UserProfile
    queryset = UserProfile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        print(self.request.method)
        if (self.request.method == 'POST'):
            return UserProfileWriteSerializer
        return UserProfileReadSerializer
