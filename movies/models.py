from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=200)
    imdb_id = models.CharField(max_length=50, null=False, blank=False)
    release_date = models.DateField(auto_now=False, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', symmetrical=False)
    imdb_rating = models.IntegerField(null=True, blank=True)
    personalities = models.ManyToManyField(Personality, related_name='filmography', symmetrical=False)
    reference_count = models.IntegerField(default=0)


class Genre(models.Model):
    genre = models.CharField(max_length=200)


class Personality(models.Model):
    PROFESSION_CHOICES = (
                      ('a', 'actor'),
                      ('d', 'director'),
                      ('w', 'writer'),
                      ('p', 'producer'),
                      ('m', 'music_director'),
                      ('ph', 'photographer'),
                      ('o', 'other'),
                      ('u', 'unspecified')
                      )
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=2, choices=PROFESSION_CHOICES, default='u')
