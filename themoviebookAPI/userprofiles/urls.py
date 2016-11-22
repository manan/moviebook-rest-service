from django.conf.urls import url
from . import views

urlpatterns = [
    url('^users/$', views.UserList.as_view(), name='UserList'),
    url('^profiles/$', views.ProfileList.as_view(), name = 'ProfileList'),
    url('^posts/$', views.PostList.as_view(), name = 'PostList'),
    url(r'^profiles/search/username=(?P<username>\w+)/$', views.ProfileByUsername.as_view()),
    url(r'^profiles/search/(?P<name>.+)/$', views.ProfileSearch.as_view()),
    url(r'^posts/search/pk=(?P<id>.+)/$', views.PostByKey.as_view()),
]
