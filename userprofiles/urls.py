from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
# from rest_framework.authtoken import views as v
from . import views

urlpatterns = [
    # ADMIN PRIVILEGES
    url('^users/$', views.UserList.as_view(), name='UserList'),
    url('^profiles/$', views.ProfileList.as_view(), name='ProfileList'),

    # ADD USER/PROFILE/
    #  url('^users/add/$', views.AddUser.as_view()),  # DEPRECATED
    #  url('^profiles/add/$', views.AddProfile.as_view()),  # DEPRECATED
    url('^signup/$', views.SignUp.as_view()),

    # GET USER DETAILS
    url(r'^users/self/$', views.SelfUser.as_view()),
    url(r'^profiles/self/$', views.SelfProfile.as_view()),

    # PROFILE PICTURES
    url(r'^profiles/profilepicture/upload/$', views.ProfilePictureUpload.as_view()),
    url(r'^profiles/profilepicture/(?P<username>\w+)/$', views.profile_picture_download),

    # SEARCH USERPROFILES
    url(r'^profiles/search/name=(?P<name>.+)/$', views.SearchProfiles.as_view()),
    url(r'^profiles/search/userpids=(?P<ids>.+)/$', views.ProfilesByIDs.as_view()),
    url(r'^profiles/search/username=(?P<username>\w+)/$', views.SearchProfileByUsername.as_view()),

    # FOLLOW/UNFOLLOW/BLOCK/UNBLOCK USERS
    #  url(r'^profiles/follow/userpid=(?P<user_pid>\w+)/$', views.follow_user), # DEPRECATED
    #  url(r'^profiles/unfollow/userpid=(?P<user_pid>\w+)/$', views.unblock_user), # DEPRECATED
    #  url(r'^profiles/block/userpid=(?P<user_pid>\w+)/$', views.block_user), # DEPRECATED
    #  url(r'^profiles/unblock/userpid=(?P<user_pid>\w+)/$', views.unblock_user), # DEPRECATED

    # UPDATE USERS/PROFILES/
    url(r'^profiles/update/$', views.UpdateProfile.as_view()),
    url(r'^users/update/$', views.UpdateUser.as_view()),

    # SPECIAL PURPOSE
    # url(r'^token-auth/$', v.obtain_auth_token),  # DEPRECATED # TokenAuthentication removed
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
]
