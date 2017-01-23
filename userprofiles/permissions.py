from rest_framework import permissions
from django.contrib.auth.models import User
from .models import UserProfile, Post

class IsOwnerOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user.profile

    def has_permission(self, request, view):
        user_id = request.user.id
        owner_id = request.data['owner']
        if owner_id is not None:
            userp = User.objects.get(id=user_id).profile
            return owner_id == userp.id
        return False

class IsUserOfProfileBeingCreated(permissions.BasePermission):
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
    def has_permission(self, request, view):
        user_id = request.user.id
        userp_user_id = request.data['user']
        if userp_user_id is not None:
            return userp_user_id == user_id
        return False
