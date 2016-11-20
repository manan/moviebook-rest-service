from rest_framework import serializers
from userprofiles.models import UserProfile, Post
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'birth_date', 'following', 'followers', 'post')

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Post
        fields = ('owner', 'movie_title', 'movie_id')
        
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = (['password'])
        read_only_fields = (['id'])

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'],
                                   email = validated_data['email'],
                                   first_name = validated_data['first_name'],
                                   last_name = validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()

        return user
