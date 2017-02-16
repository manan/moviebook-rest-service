from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as view

urlpatterns = [
    # ADMIN PRIVILEGES
    url('^users/$', views.UserList.as_view(), name='UserList'),
    url('^profiles/$', views.ProfileList.as_view(), name = 'ProfileList'),
    url('^posts/$', views.PostList.as_view(), name = 'PostList'),

    # ADD USER/PROFILE/POST
    url('^users/add/$', views.AddUser.as_view()),
    url('^profiles/add/$', views.AddProfile.as_view()),
    url('^posts/add/$', views.AddPost.as_view()),

    # GET USER DETAILS
    url(r'^users/fetchdetails/$', views.SelfUserDetails.as_view()),
    url(r'^profiles/fetchdetails/$', views.SelfProfileDetails.as_view()),

    # SEARCH USERPROFILES
    url(r'^profiles/search/name=(?P<name>.+)/$', views.SearchProfiles.as_view()),
    url(r'^profiles/search/userpids=(?P<ids>.+)/$', views.ProfilesByIDs.as_view()),
    url(r'^profiles/search/username=(?P<username>\w+)/$', views.SearchProfileByUsername.as_view()),

    # SEARCH POSTS
    url(r'^posts/search/username=(?P<username>.+)/$', views.PostsByUsername.as_view()),
    url(r'^posts/search/userpid=(?P<userpid>.+)/$', views.PostsByUserPId.as_view()),
    url(r'^posts/search/postids=(?P<ids>.+)/$', views.PostsByIDs.as_view()),

    # FOLLOW/UNFOLLOW/BLOCK/UNBLOCK USERS # Don't use for production server
    url(r'^profiles/follow/userpid=(?P<userpid>\w+)/$', views.FollowUser),
    url(r'^profiles/unfollow/userpid=(?P<userpid>\w+)/$', views.UnfollowUser),
    url(r'^profiles/block/userpid=(?P<userpid>\w+)/$', views.BlockUser),
    url(r'^profiles/unblock/userpid=(?P<userpid>\w+)/$', views.UnblockUser),

    # UPDATE USERS/PROFILES/POSTS
    url(r'^profiles/update/$', views.UpdateProfile.as_view()),
    url(r'^posts/update/postpk=(?P<pk>.+)/$', views.UpdatePost.as_view()),
    url(r'^users/update/$', views.UpdateUser.as_view()),

    # DELETE POSTS
    url(r'^posts/delete/postpk=(?P<pk>.+)/$', views.DeletePost.as_view()),

    # SPECIAL PURPOSE
    url(r'^newsfeed/$', views.NewsFeed.as_view()),
    url(r'^token-auth/$', view.obtain_auth_token),

    # PROFILE PICTURES
    url(r'^profilepicture/upload/$', views.ProfilePictureUpload.as_view()),
    url(r'^profilepicture/(?P<username>\w+)/$', views.ProfilePictureDownload)
    
]
