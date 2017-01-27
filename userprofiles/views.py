from django.shortcuts import render
from rest_framework import generics, permissions

from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile, Post
from .serializers import UserProfileReadSerializer, UserProfileWriteSerializer
from .serializers import RegistrationSerializer, PostSerializer
from .permissions import IsOwnerOrReadOnly
from .permissions import IsUserOfProfileBeingCreated
from django.contrib.auth.models import User

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from django.db.models import Q

from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from datetime import datetime
from datetime import timedelta

# Create your views here.

class ProfilePicture(APIView):
    """
    https://themoviebook.herokuapp.com/profilepicture/upload/
    POST Request:
    curl -i -H "Authorization: Token e0e4a26da62d55c0b017138dfd3f18b96a9fe58a" -F "file=@icon.jpg" 
    http://127.0.0.1:8000/profilepicture/upload/
    
    To upload a profile picture for authenticated user
    """
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        userprofile = request.user.profile
        userprofile.profile_picture.delete()
        userprofile.profile_picture = file_obj
        userprofile.save()
        return Response(status=204)

#require_http_methods(['GET'])
class NewsFeed(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/newsfeed/
    GET request: returns the newsfeed for active user

    Required Keys for GET: none
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        people_following = self.request.user.profile.followings.all()
        newsfeed = []
        for person in people_following:
            for post in person.post.filter(upload_date__gte=datetime.now() - timedelta(days=2)):
                newsfeed.append(post)
        newsfeed.sort(key=lambda x: x.upload_date, reverse=True)
        return newsfeed

#require_http_methods(['DELETE'])
class DeletePost(generics.DestroyAPIView):
    """
    https://themoviebook.herokuapp.com/posts/delete/postpk=<pk>/
    DELETE request: deletes post with the given pk

    Required Keys for DELETE: none

    On invalid pk: {"detail":"Not found."}
    On invalid user (not owner): { "detail": "You do not have permission to perform this action." }
    """
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

#['PUT', 'PATCH']
class UpdateUser(generics.UpdateAPIView):
    """
    https://themoviebook.herokuapp.com/users/update/
    PATCH request: modifies active user
    DO NOT USE PUT

    Required Keys for PATCH: none except the ones you want to change
    """
    model = User
    serializer_class = RegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def perform_update(self, serializer):                                                           
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])                                 
            serializer.save(password=password)                                                      
        else:
            serializer.save()

    def get_object(self):
        return self.request.user
    
#['PUT', 'PATCH']
class UpdatePost(generics.UpdateAPIView):
    """
    https://themoviebook.herokuapp.com/posts/update/postpk=<pk>/
    PATCH request: Updates post with given pk
    DO NOT USE PUT

    Required Keys for PATCH: only the ones you want to change

    On invalid user (not owner): { "detail": "You do not have permission to perform this action." }
    """
    model = Post
    serializer_class = PostSerializer
    lookup_field = 'pk'
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        return self.request.user.profile.post.all()

#['PUT', 'PATCH']
class UpdateProfile(generics.UpdateAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/update/
    PATCH request: modifies active user
    DO NOT USE PUT

    Required Keys for PATCH: none except the ones you want to change
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user.profile

#require_http_methods(['GET'])
@csrf_exempt
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def UnfollowGET(request, username):
    """
    GET request: result: authenticated user unfollows user w username

    Required Keys for GET: username

    On invalid username: 412 Precondition Failed
    On invalid method: 405 Method not allowed 
    If not formatted properly: 412 Precondition Failed
    If username2 doesn't follow username1: 412 Precondition Failed
    """
    try:
        userp = request.user.profile
        bool = userp.unfollow(username)
        if bool:
            return HttpResponse('Done!', status=status.HTTP_200_OK)
        else:
            return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception:
        return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)

#require_http_methods(['GET'])
@csrf_exempt
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,)) 
def FollowGET(request, username):
    """
    GET request: result: authenticated user follows user w username

    Required Keys for GET: username

    On invalid username: 412 Precondition Failed
    On invalid method: 405 Method not allowed 
    If not formatted properly: 412 Precondition Failed
    If username2 doesn't follow username1: 412 Precondition Failed
    """
    try:
        userp = request.user.profile
        bool = userp.follow(username)
        if bool:
            return HttpResponse('Done!', status=status.HTTP_200_OK)
        else:
            return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception:
        return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)

#require_http_methods(['GET'])
@csrf_exempt
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def UnblockGET(request, username):
    """
    GET request: result: authenticated user unblocks user w username

    Required Keys for GET: username

    On invalid username: 412 Precondition Failed
    On invalid method: 405 Method not allowed 
    If not formatted properly: 412 Precondition Failed
    If username2 doesn't follow username1: 412 Precondition Failed
    """
    try:
        userp = request.user.profile
        bool = userp.unblock(username)
        if bool:
            return HttpResponse('Done!', status=status.HTTP_200_OK)
        else:
            return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception:
        return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)

#require_http_methods(['GET'])
@csrf_exempt
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def BlockGET(request, username):
    """
    GET request: result: authenticated user blocks user w given username

    Required Keys for GET: username

    On invalid username: 412 Precondition Failed
    On invalid method: 405 Method not allowed 
    If not formatted properly: 412 Precondition Failed
    If username2 doesn't follow username1: 412 Precondition Failed
    """
    try:
        userp = request.user.profile
        bool = userp.block(username)
        if bool:
            return HttpResponse('Done!', status=status.HTTP_200_OK)
        else:
            return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)
    except Exception:
        return HttpResponse('Failed!', status=status.HTTP_412_PRECONDITION_FAILED)

#['GET']
class PostsByUserPId(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/posts/search/userpid=<id>/
    GET request fetches all the posts of a certain user

    Required Keys for GET: <user id>

    On invalid user: []
    No ids mentioned: 404 Page not found
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        queryuser = UserProfile.objects.get(pk=self.kwargs['userpid'])
        if self.request.user.profile.isBlockedBy(queryuser.user.username):
            raise Exception("The user you're trying to find has blocked you. Savage. Lmao.");
        return queryuser.post.all()

#['GET']
class PostsByUsername(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/posts/search/username=<username>/
    GET request fetches all the posts of the given user
    Raises Exception if active user is blocked by the queried user.

    Required Keys for GET: <username>

    On invalid user: []
    No ids mentioned: 404 Page not found
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        if request.user.profile.isBlockedBy(username=self.kwargs['username']):
            raise Exception("The user you're trying to find has blocked you. Savage. Lmao.");
        queryuser = User.objects.get(username=self.kwargs['username']).profile
        return queryuser.post.all()

#['GET']
class PostsByIDs(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/posts/search/postids=<id1>,<id2>...<idn>/
    GET request fetches all the posts with the given post ids

    Required Keys for GET: at least one id

    On no match: []
    No ids mentioned: 404 Page not found
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
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

#['GET']
class ProfilesByIDs(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/search/userpids=<id1>,<id2>,..<idn>/
    GET request fetches the users with the given user ids. Set doesn't include
    profiles that have blocked active user.

    Required Keys for GET: at least one id

    On no matches: []
    No ids mentioned: 404 Page not found
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        ids = self.kwargs['ids'].replace(' ', '').split(',')
        ids = [int(every) for every in ids]
        ret = set()
        for everyid in ids:
            try:
                userprofile = UserProfile.objects.get(pk=everyid)
                if not self.request.user.profile.isBlockedBy(userprofile.user.username):
                    ret.add(UserProfile.objects.get(pk=everyid))
            except (UserProfile.DoesNotExist):
                pass
        return ret

#['GET']
class SearchProfiles(generics.ListAPIView): # DONE
    """
    https://themoviebook.herokuapp.com/profiles/search/name=<name>/
    GET request fetches all the userprofiles with an approximate 
    name match. Set doesn't include profiles that have blocked active user.

    Required Keys for GET: <name>

    On no matches: []
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        name = self.kwargs['name'].strip()
        ret = set()
        if (len(name.split(' ')) == 1):
            for every in User.objects.filter(Q(first_name__icontains = name)
                                             | Q(last_name__icontains = name)
                                             | Q(username__icontains = name)):
                if not self.request.user.profile.isBlockedBy(every.username):
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
                if not self.request.user.profile.isBlockedBy(every.username):
                    ret.add(every.profile)
        return ret

#['GET']
class SearchProfileByUsername(generics.RetrieveAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/search/username=<username>/
    GET: returns userprofile object with the given username, serialized
    Exception raised when user is blocked by the user he is searching for.
    Required Keys for GET: <username>

    On no match: []
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_object(self):
        if (self.request.user.profile.isBlockedBy(self.kwargs['username'])):
            raise Exception("The user you're trying to find has blocked you. Savage. Lmao.")
        result = User.objects.get(username=self.kwargs['username']).profile

#['GET']
class SelfDetails(generics.RetrieveAPIView):
    """
    https://themoviebook.herokuapp.com/users/fetchdetails/
    GET: returns authenticated user object, serialized
    """
    model = User
    serializer_class = RegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user

#['POST']
class AddUser(generics.CreateAPIView):
    """
    https://themoviebook.herokuapp.com/users/add/
    POST request body {"username":<>, "password":<>, "email":<>, "first_name":<>, "last_name":<>}
    adds user to the db

    Required Keys for POST: username, password, email, first_name, last_name

    On used username: {"username":["A user with that username already exists."]}
    On missing any fields: 500 Internal Server Error
    """
    model = User
    serializer_class = RegistrationSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

#['POST']
class AddPost(generics.CreateAPIView):
    """
    https://themoviebook.herokuapp.com/posts/add/
    POST request body: {"owner":<userpid>, "movie_title":<bio>, "movie_id":"<imdbid>", "caption":"<cap>"}
    adds post (with owner being the userp specified) to the db

    Required Keys for POST: user, movie_id

    On invalid user: {"user":["Invalid pk \"4\" - object does not exist."]}
    On missing movie_id field: {"movie_id":["This field is required."]}
    On missing owner field: {"owner":["This field is required."]}
    On denied permission: {...}
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

#['POST']
class AddProfile(generics.CreateAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/add/
    POST request body: {"user":<userid>, "bio":<bio>, "birth_date":"<YYYY-MM-DD>"}
    adds profile to db

    Required Keys for POST: user

    If user id already has a profile: {"user":["This field must be unique."]}
    On invalid user: {"user":["Invalid pk \"4\" - object does not exist."]}
    On denied permission: {...}
    """
    model = UserProfile
    serializer_class = UserProfileWriteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
        IsUserOfProfileBeingCreated,
    ]

#['GET']
class UserList(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/users/
    GET request fetches all the users in the db
    
    Authentication: Restricted to admin users only
    """
    model = User
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
    ]

#['GET']
class PostList(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/posts/
    GET request fetches all the posts of the all the users in the db

    Authentication: Restricted to admin users only
    """
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
    ]

#['GET']
class ProfileList(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/
    GET request fetches the userprofiles of the all the users in the db

    Authentication: Restricted to admin users only 
    """
    model = UserProfile
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
    ]
    
    def get_serializer_class(self):
        if (self.request.method == 'POST'):
            return UserProfileWriteSerializer
        return UserProfileReadSerializer
