from rest_framework import serializers
from asura.models import Post
from asura.serializers.post_media_serializer import PostMediaSerializer

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a Post model serializer
    """
    user_uuid = serializers.CharField(source='user.uuid')
    user_username = serializers.CharField(source='user.username')
    user_firstname = serializers.CharField(source='user.first_name')
    user_lastname = serializers.CharField(source='user.last_name')
    user_score = serializers.IntegerField(source='get_user_score')
    media = PostMediaSerializer(source='media_files', many=True) # media _set

    class Meta:
        model = Post
        fields = [
            'uuid',
            'created_at',
            'content',
            'likes_count',
            'user_uuid',
            'user_username',
            'user_firstname',
            'user_lastname',
            'user_score',
            'media'
        ]
