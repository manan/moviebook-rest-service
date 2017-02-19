from rest_framework import permissions
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user.profile

    def has_permission(self, request, view):
        user_id = request.user.id
        owner_id = request.data['owner']
        if owner_id is not None:
            user_profile = User.objects.get(id=user_id).profile
            return owner_id == user_profile.id
        return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user.profile

    def has_permission(self, request, view):
        user_id = request.user.id
        owner_id = request.data['owner']
        if owner_id is not None:
            user_profile = User.objects.get(id=user_id).profile
            return owner_id == user_profile.id
        return False
