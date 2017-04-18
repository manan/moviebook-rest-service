from rest_framework import serializers
from .models import UserProfile, Activation
from django.contrib.auth.models import User
from posts.serializers import PostSerializer

class ActivationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activation
        fields = ('user', 'key', 'expires', 'id')


class UserProfileReadSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('user', 'username', 'first_name', 'last_name', 'email', 'gender', 'bio', 'birth_date',
                  'profile_picture', 'followings', 'followers', 'id')


class UserProfileSelfReadSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    posts = PostSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'username', 'first_name', 'last_name', 'email', 'gender', 'bio', 'birth_date',
                  'profile_picture', 'followings', 'followers', 'blocked', 'blocked_by', 'id')


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'gender', 'bio', 'birth_date')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'gender', 'bio', 'birth_date', 'profile_picture', 'followings', 'blocked')


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = (['password'])
        read_only_fields = (['id'])

    def create(self, validated_data):
            user = User.objects.create(username=validated_data['username'],
                                       email=validated_data['email'],
                                       first_name=validated_data['first_name'],
                                       last_name=validated_data['last_name'])
            user.set_password(validated_data['password'])
            user.save()
            return user
