from rest_framework import permissions


class IsUserOfProfile(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
    
    def has_permission(self, request, view):
        user_id = request.user.id
        user_profile_user_id = request.data['user']
        if user_profile_user_id is not None:
            return user_profile_user_id == user_id
        return False
