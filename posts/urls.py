from django.conf.urls import url
from . import views

urlpatterns = [
    # ADMIN PRIVILEGES
    url('^$', views.PostList.as_view(), name='PostList'),

    # ADD USER/PROFILE/POST
    url('^add/$', views.AddPost.as_view()),

    # Add like and comment
    url('^like/profile=(?<owner_id>.+)/postid=(?P<pid>.+)/rating=(?P<ra>.+)/$', views.like_post),
    url('^comment/profile=(?<owner_id>.+)/postid=(?P<pid>.+)/comment=(?P<co>.+)/$', views.comment_post),

    # SEARCH POSTS
    url(r'^search/username=(?P<username>.+)/$', views.PostsByUsername.as_view()),
    url(r'^search/userpid=(?P<userpid>.+)/$', views.PostsByUserPId.as_view()),
    url(r'^search/postids=(?P<ids>.+)/$', views.PostsByPostIDs.as_view()),

    # UPDATE USERS/PROFILES/POSTS
    url(r'^update/(?P<pk>.+)/$', views.UpdatePost.as_view()),

    # DELETE POSTS
    url(r'^delete/(?P<pk>.+)/$', views.DeletePost.as_view()),
    url(r'^newsfeed/$', views.NewsFeed.as_view()),
]
