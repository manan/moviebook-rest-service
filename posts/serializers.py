from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='owner.user.username')
    profile_picture = serializers.ReadOnlyField(source='owner.user.profile.profile_picture.url')

    class Meta:
        model = Post
        fields = ('owner', 'username', 'profile_picture', 'movie_title', 'movie_id', 'caption',
                  'upload_date', 'id')
