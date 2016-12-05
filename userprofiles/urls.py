from django.conf.urls import url
from . import views

urlpatterns = [
    url('^users/$', views.UserList.as_view(), name='UserList'),
    url('^profiles/$', views.ProfileList.as_view(), name = 'ProfileList'),
    url('^posts/$', views.PostList.as_view(), name = 'PostList'),
    
    url(r'^profiles/search/name=(?P<name>.+)/$', views.SearchProfiles.as_view()),
    url(r'^profiles/search/userids=(?P<ids>.+)/$', views.ProfilesByIDs.as_view()),

    url(r'^posts/search/userid=(?P<id>.+)/$', views.PostsOfUser.as_view()),
    url(r'^posts/search/postids=(?P<ids>.+)/$', views.PostsByIDs.as_view()),

    url(r'^profiles/follow/username1=(?P<username1>\w+)/username2=(?P<username2>\w+)/$', views.AddFollowerGET),
    url(r'^profiles/follow/username1=(?P<username1>\w+)/username2=(?P<username2>\w+)/remove/$', views.RemoveFollowerGET),

    url(r'^posts/update/postpk=(?P<pk>.+)/$', views.UpdatePost.as_view()),

    url(r'^posts/delete/postpk=(?P<pk>.+)/$', views.DeletePost.as_view()),

    url(r'^newsfeed/userid=(?P<userid>.+)/$', views.NewsFeed.as_view()),
]
