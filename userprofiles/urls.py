from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as view

urlpatterns = [
    # ADMIN PRIVILEGES
    url('^users/$', views.UserList.as_view(), name='UserList'),
    url('^profiles/$', views.ProfileList.as_view(), name='ProfileList'),

    # ADD USER/PROFILE/
    url('^users/add/$', views.AddUser.as_view()),
    url('^profiles/add/$', views.AddProfile.as_view()),

    # GET USER DETAILS
    url(r'^users/fetchdetails/$', views.SelfUserDetails.as_view()),
    url(r'^profiles/fetchdetails/$', views.SelfProfileDetails.as_view()),

    # PROFILE PICTURES
    url(r'^profilepicture/upload/$', views.ProfilePictureUpload.as_view()),
    url(r'^profilepicture/(?P<username>\w+)/$', views.profile_picture_download),

    # SEARCH USERPROFILES
    url(r'^profiles/search/name=(?P<name>.+)/$', views.SearchProfiles.as_view()),
    url(r'^profiles/search/userpids=(?P<ids>.+)/$', views.ProfilesByIDs.as_view()),
    url(r'^profiles/search/username=(?P<username>\w+)/$', views.SearchProfileByUsername.as_view()),

    # FOLLOW/UNFOLLOW/BLOCK/UNBLOCK USERS # Don't use for production server
    url(r'^profiles/follow/userpid=(?P<userpid>\w+)/$', views.follow_user),
    url(r'^profiles/unfollow/userpid=(?P<userpid>\w+)/$', views.unblock_user),
    url(r'^profiles/block/userpid=(?P<userpid>\w+)/$', views.block_user),
    url(r'^profiles/unblock/userpid=(?P<userpid>\w+)/$', views.unblock_user),

    # UPDATE USERS/PROFILES/
    url(r'^profiles/update/$', views.UpdateProfile.as_view()),
    url(r'^users/update/$', views.UpdateUser.as_view()),

    # SPECIAL PURPOSE
    url(r'^token-auth/$', view.obtain_auth_token),
]
