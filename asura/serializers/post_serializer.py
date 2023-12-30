from rest_framework import serializers
from asura.models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a Post model serializer
    """
    user_uuid = serializers.CharField(source='user.uuid')
    user_username = serializers.CharField(source='user.username')
    user_firstname = serializers.CharField(source='user.first_name')
    user_lastname = serializers.CharField(source='user.last_name')

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
            'user_lastname'
        ]

