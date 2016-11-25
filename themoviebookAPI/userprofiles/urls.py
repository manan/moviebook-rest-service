from django.conf.urls import url
from . import views

urlpatterns = [
    url('^users/$', views.UserList.as_view(), name='UserList'),
    url('^profiles/$', views.ProfileList.as_view(), name = 'ProfileList'),
    url('^posts/$', views.PostList.as_view(), name = 'PostList'),
    
    url(r'^profiles/search/username=(?P<username>\w+)/$', views.ProfileByUsername.as_view()),
    url(r'^profiles/search/name=(?P<name>.+)/$', views.SearchProfiles.as_view()),
    url(r'^profiles/search/userids=(?P<ids>.+)/$', views.ProfilesByIDs.as_view()),

    url(r'^posts/search/userid=(?P<id>.+)/$', views.PostsOfUser.as_view()),
    url(r'^posts/search/postids=(?P<ids>.+)/$', views.PostsByIDs.as_view()),
]
