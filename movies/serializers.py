from rest_framework import serializers
from .models import Movie, Genre, Personality


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'genre')


class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = ('id', 'name', 'role')


class MovieWriteSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'imdb_id', 'release_date', 'runtime', 'imdb_rating')


class MovieWriteExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'imdb_id', 'release_date', 'runtime', 'genres',
                  'imdb_rating', 'personalities', 'reference_count')


class MovieReadSerializer(serializers.ModelSerializer):
    personalities = PersonalitySerializer(source='personalities', many=True)
    genres = GenreSerializer(source='genres', many=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'imdb_id', 'release_date', 'runtime', 'genres',
                  'imdb_rating', 'personalities', 'reference_count')
