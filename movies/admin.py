from django.contrib import admin
from .models import Movie, Personality, Genre

# Register your models here

admin.site.register(Movie)
admin.site.register(Personality)
admin.site.register(Genre)
