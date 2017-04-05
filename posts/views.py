from datetime import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Post
from userprofiles.models import UserProfile

from .serializers import PostSerializer

from .permissions import IsOwnerOrReadOnly, IsOwner

from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
# Create your views here.


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def like_post(request, pid, ra, owner_id):
    """
    https://themoviebook.herokuapp.com/posts/like/userpid=<>/postid=<>/rating=<>/
    GET request: adds Like
    """
    try:
        profile = request.user.profile
        post_owner = UserProfile.objects.get(pk=owner_id)
        post = post_owner.posts.get(pk=pid)
        post.like(profile, ra)
        return JsonResponse({'detail': 'successful'}, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'detail': 'failed'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def comment_post(request, pid, co, owner_id):
    """
    https://themoviebook.herokuapp.com/posts/comment/userpid=<>/postid=<>/rating=<>/
    GET request: Adds comment
    """
    try:
        profile = request.user.profile
        post_owner = UserProfile.objects.get(pk=owner_id)
        post = post_owner.posts.get(pk=pid)
        post.comment(profile, co)
        return JsonResponse({'detail': 'successful'}, safe=False, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse({'detail': 'failed'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ['GET']
class NewsFeed(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/newsfeed/
    GET request: returns the newsfeed for active user

    Required Keys for GET: none
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        people_following = self.request.user.profile.followings.all()
        newsfeed = []
        for person in people_following:
            for post in person.posts.filter(upload_date__gte=datetime.now() - timedelta(days=2)):
                newsfeed.append(post)
        newsfeed.sort(key=lambda x: x.upload_date, reverse=True)
        return newsfeed


# ['DELETE']
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
    lookup_field = 'pk'
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
    ]

    def get_queryset(self):
        return self.request.user.profile.posts.all()


# ['PUT', 'PATCH']
class UpdatePost(generics.UpdateAPIView):
    """
    https://themoviebook.herokuapp.com/posts/update/postpk=<pk>/
    PATCH/PUT request: Updates post with given pk

    Required Keys for PATCH: only the ones you want to change

    On invalid user (not owner): { "detail": "You do not have permission to perform this action." }
    """
    model = Post
    serializer_class = PostSerializer
    lookup_field = 'pk'
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner
    ]

    def get_queryset(self):
        return self.request.user.profile.posts.all()


# ['GET']
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
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        query_user = UserProfile.objects.get(pk=self.kwargs['userpid'])
        if self.request.user.profile.is_blocked_by(username=query_user.user.username):
            raise Exception("The user you're trying to find has blocked you. Savage. Lmao.")
        return query_user.posts.all()


# ['GET']
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
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        if self.request.user.profile.is_blocked_by(username=self.kwargs['username']):
            raise Exception("The user you're trying to find has blocked you. Savage. Lmao.")
        query_user = User.objects.get(username=self.kwargs['username']).profile
        return query_user.posts.all()


# ['GET']
class PostsByPostIDs(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/posts/search/postids=<id1>,<id2>...<idn>/
    GET request fetches all the posts with the given post ids

    Required Keys for GET: at least one id

    On no match: []
    No ids mentioned: 404 Page not found
    """
    model = Post
    serializer_class = PostSerializer
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
                temp_post = Post.objects.get(pk=every_id)
                if not self.request.user.profile.is_blocked_by(upid=temp_post.owner):
                    ret.add(Post.objects.get(pk=every_id))
            except Post.DoesNotExist:
                pass
        return ret


# ['POST']
class AddPost(generics.CreateAPIView):
    """
    https://themoviebook.herokuapp.com/posts/add/
    POST request body: {"owner":<userpid>, "movie_title":<bio>, "imdb_id":"<imdbid>", "caption":"<cap>"}
    adds post (with owner being the userp specified) to the db

    Required Keys for POST: owner, imdb_id

    If Post.owner != self.request.user, permission denied
    """
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    ]


# ['GET']
class PostList(generics.ListAPIView):
    """
    Admin only

    https://themoviebook.herokuapp.com/posts/
    GET request fetches all the posts of the all the users in the db
    """
    model = Post
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAdminUser,
    ]
