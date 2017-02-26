from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='owner.user.username')

    class Meta:
        model = Post
        fields = ('owner', 'username', 'movie_title', 'imdb_id', 'caption',
                  'upload_date', 'id')
