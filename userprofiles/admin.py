from django.contrib import admin
from .models import UserProfile, Activation

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Activation)
