from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserProfile

from .serializers import UserProfileReadSerializer, UserProfileCreateSerializer
from .serializers import UserProfileUpdateSerializer, UserProfileSelfReadSerializer
from .serializers import RegistrationSerializer

from .permissions import IsUserOfProfile

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions
# Create your views here.


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def profile_picture_download(request, username):
    if request.user.profile.is_blocked_by(username):
        return Response({"detail": "User is blocked."}, status=403)
    try:
        image_url = User.objects.get(username=username).profile.profile_picture.url
        return render(request, "profilepicture.html", {'imageurl': image_url})
    except User.DoesNotExist:
        return HttpResponse('{"detail": "User not found."}')


# ['POST']
class ProfilePictureUpload(APIView):
    """
    https://themoviebook.herokuapp.com/profilepicture/upload/
    sets image as logged in user's profile picture

    Demo Request:
    curl -i -H "Authorization: JWT <token>" -F "file=@icon.jpg" /profilepicture/upload/
    """
    parser_classes = (FormParser, MultiPartParser)
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        #  Check if FILES contains key
        file_obj = request.FILES['file']
        user_profile = self.request.user.profile
        user_profile.profile_picture = file_obj
        user_profile.save()
        return Response(UserProfileReadSerializer(user_profile).data, status=200)


# ['PUT', 'PATCH']
class UpdateUser(generics.UpdateAPIView):
    """
    https://themoviebook.herokuapp.com/users/update/
    PATCH/PUT request: modifies active user

    Required Keys for PATCH: none except the ones you want to change
    """
    model = User
    serializer_class = RegistrationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):                                                           
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])                                 
            serializer.save(password=password)                                                      
        else:
            serializer.save()


# ['PUT', 'PATCH']
class UpdateProfile(generics.UpdateAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/update/
    modifies logged-in-user
    
    Required Keys for PATCH: none except the ones you want to change
    Required Keys for PUT:
    """
    model = UserProfile
    serializer_class = UserProfileUpdateSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        user_profile = self.request.user.profile
        new_followings = user_profile.followings.all()
        new_blocked = user_profile.blocked.all()
        if 'followings' in self.request.data:
            new_followings = []
            for following in self.request.data['followings']:
                if not user_profile.is_blocked_by(upid=following):
                    new_followings.append(following)
        if 'blocked' in self.request.data:
            new_blocked = []
            for b in self.request.data['blocked']:
                user_profile.remove_follower(upid=b)
                new_blocked.append(b)
        serializer.save(user=user_profile.user.id, followings=new_followings, blocked=new_blocked)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated, IsUserOfProfile))
def unfollow_user(request, user_pid):
    """
    DEPRECATED

    GET request: logged in user unfollows user w provided user_pid

    Required Keys for GET: user_pid
    """
    try:
        user_profile = request.user.profile
        user_profile.unfollow(upid=user_pid)
        return HttpResponse(UserProfileReadSerializer(user_profile).data, status=200)
    except Exception:
        return Response(status=500)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated, IsUserOfProfile))
def follow_user(request, user_pid):
    """
    DEPRECATED

    GET request: logged in user follows user w provided user_pid

    Required Keys for GET: user_pid
    """
    try:
        user_profile = request.user.profile
        user_profile.follow(upid=user_pid)
        return HttpResponse(UserProfileReadSerializer(user_profile).data, status=200)
    except Exception:
        return Response(status=500)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated, IsUserOfProfile))
def unblock_user(request, user_pid):
    """
    DEPRECATED

    GET request: logged in user unblocks user w provided user_pid

    Required Keys for GET: user_pid
    """
    try:
        user_profile = request.user.profile
        user_profile.unblock(upid=user_pid)
        return HttpResponse(UserProfileReadSerializer(user_profile).data, status=200)
    except Exception:
        return Response(status=500)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated, IsUserOfProfile))
def block_user(request, user_pid):
    """
    DEPRECATED

    GET request: logged in user blocks user w provided user_pid

    Required Keys for GET: user_pid
    """
    try:
        user_profile = request.user.profile
        user_profile.block(upid=user_pid)
        return Response(UserProfileReadSerializer(user_profile).data, status=200)
    except Exception:
        return Response(status=500)


# ['GET']
class ProfilesByIDs(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/search/userpids=<id1>,<id2>,..<idn>/
    Gets users with the given user ids. Set doesn't include users who have blocked
    logged in user

    Required Keys for GET: at least one id

    On no matches: []
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        ids = self.kwargs['ids'].replace(' ', '').split(',')
        ids = [int(every) for every in ids]
        ret = set()
        for every_id in ids:
            try:
                user_profile = UserProfile.objects.get(pk=every_id)
                if not self.request.user.profile.is_blocked_by(upid=user_profile.id):
                    ret.add(user_profile)
            except UserProfile.DoesNotExist:
                pass
        return ret


# ['GET']
class SearchProfiles(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/search/name=<name>/
    Gets all the userprofiles with an approximate name match.
    Doesn't include profiles that have blocked logged in user.

    Required Keys for GET: name

    On no matches: []
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        name = self.kwargs['name'].strip()
        ret = set()
        if len(name.split(' ')) == 1:
            for every in User.objects.filter(Q(first_name__icontains=name)
                                             | Q(last_name__icontains=name)
                                             | Q(username__icontains=name)):
                if not self.request.user.profile.is_blocked_by(username=every.username):
                    ret.add(every.profile)
        elif len(name.split(' ')) >= 2:
            fname = name.split(' ')[0]
            lname = name.split(' ')[1]
            for every in User.objects.filter(Q(first_name__contains=fname) |
                                             Q(last_name__contains=lname) |
                                             Q(first_name__contains=lname) |
                                             Q(last_name__contains=fname) |
                                             Q(username__contains=fname) |
                                             Q(username__contains=lname)):
                if not self.request.user.profile.is_blocked_by(username=every.username):
                    ret.add(every.profile)
        return ret


# ['GET']
class SearchProfileByUsername(generics.RetrieveAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/search/username=<username>/
    Gets models.UserProfile if found an exact match

    Exception raised if logged in user is blocked by user he is searching for
    Exception raised if user not found

    Required Keys for GET: username
    """
    model = UserProfile
    serializer_class = UserProfileReadSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        if self.request.user.profile.is_blocked_by(username=self.kwargs['username']):
            raise Exception("The user you're trying to find has blocked you.")
        return User.objects.get(username=self.kwargs['username']).profile


# ['GET']
class SelfUser(generics.RetrieveAPIView):
    """
    https://themoviebook.herokuapp.com/users/self/
    Gets auth.User of logged in user
    """
    model = User
    serializer_class = RegistrationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user


# ['GET']
class SelfProfile(generics.RetrieveAPIView):
    """
    https://themoviebook.herokuapp.com/profiles/self/
    Gets models.UserProfile of logged in user
    """
    model = UserProfile
    serializer_class = UserProfileSelfReadSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]
        
    def get_object(self):
        return self.request.user.profile


# ['POST']
class AddProfile(generics.CreateAPIView):
    """
    DEPRECATED

    https://themoviebook.herokuapp.com/profiles/add/
    adds UserProfile to db

    Required Keys for POST: user

    If user.id != UserProfile.user, permission denied
    """
    model = UserProfile
    serializer_class = UserProfileCreateSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
        # permissions.IsAuthenticated,
        # IsUserOfProfile,
    ]


# ['POST']
class AddUser(generics.CreateAPIView):
    """
    DEPRECATED

    https://themoviebook.herokuapp.com/users/add/
    POST request body {"username":<>, "password":<>, "email":<>, "first_name":<>, "last_name":<>}
    adds user to the db

    Required Keys for POST: username, password, email, first_name, last_name
    """
    model = User
    serializer_class = RegistrationSerializer
    permission_classes = [
        permissions.IsAdminUser,
        # permissions.AllowAny,
    ]


# ['POST']
class SignUp(APIView):
    """
    https://themoviebook.herokuapp.com/signup/
    Adds User and UserProfile to db

    Required Keys for POST: username, password, first_name, last_name, email, gender
    """
    permission_classes = [
        permissions.AllowAny,
    ]

    @ratelimit(key='ip', rate='2/m', block=True)
    def post(self, request):
        # Checking for validity
        errors = dict()
        try:
            validate_email(self.request.data['email'])
        except ValidationError as e:
            errors['email'] = ["Enter a valid email address."]
        if User.objects.filter(username=self.request.data['username']).exists():
            errors["username"] = ["A user with that username already exists."]
        if 'email' in errors.keys() or 'username' in errors.keys():
            return Response(data=errors, status=400)
        # Can move forward with signing up

        u = User(username=self.request.data['username'],
                 email=self.request.data['email'],
                 first_name=self.request.data['first_name'],
                 last_name=self.request.data['last_name'])
        u.set_password(self.request.data['password'])
        u.save()
        user_profile = UserProfile(id=u.id, user=u, gender=self.request.data['gender'], birth_date='1900-01-01')
        user_profile.save()
        return Response(data=RegistrationSerializer(u).data, status=200)


# ['GET']
class UserList(RatelimitMixin, generics.ListAPIView):
    """
    ADMIN ONLY

    https://themoviebook.herokuapp.com/users/
    Gets auth.User of all users in db
    """
    ratelimit_key = 'ip'
    ratelimit_rate = '1/15s'
    ratelimit_block = True
    ratelimit_method = 'GET'

    model = User
    queryset = User.objects.all().order_by('id')
    serializer_class = RegistrationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
    ]


# ['GET']
class ProfileList(RatelimitMixin, generics.ListAPIView):
    """
    ADMIN ONLY

    https://themoviebook.herokuapp.com/profiles/
    Gets UserProfile of the all users in db
    """
    ratelimit_key = 'ip'
    ratelimit_rate = '1/15s'
    ratelimit_block = True
    ratelimit_method = 'GET'

    model = UserProfile
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserProfileReadSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
    ]
