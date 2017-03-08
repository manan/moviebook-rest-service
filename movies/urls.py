from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MoviesList.as_view()),
    url(r'^genres/$', views.GenreList.as_view()),
    url(r'^personalities/$', views.PersonalityList.as_view()),
    url(r'^add/$', views.AddMovie.as_view()),
]
