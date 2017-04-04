# from django.shortcuts import render
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import MovieReadSerializer, MovieWriteSimpleSerializer
from .serializers import GenreSerializer, PersonalitySerializer
from .models import Movie, Genre, Personality

from rest_framework import generics

# Create your views here.


# ['POST']
class AddMovie(generics.CreateAPIView):
    """
    https://themoviebook.herokuapp.com/movies/add/

    Required Keys for POST: ...
    """
    model = Movie
    serializer_class = MovieWriteSimpleSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated,
    ]


# ['GET']
class MoviesList(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/movies/
    """
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieReadSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (
        permissions.IsAdminUser,
    )


# ['GET']
class GenreList(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/movies/genres/
    """
    model = Genre
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (
        permissions.IsAdminUser,
    )


# ['GET']
class PersonalityList(generics.ListAPIView):
    """
    https://themoviebook.herokuapp.com/movies/personalities/
    """
    model = Personality
    queryset = Personality.objects.all()
    serializer_class = PersonalitySerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (
        permissions.IsAdminUser,
    )