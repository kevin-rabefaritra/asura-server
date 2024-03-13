from rest_framework import serializers
from asura.models import Post
from asura.serializers.post_media_serializer import PostMediaSerializer
from asura.serializers.users_serializer import UserSummarySerializer

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a Post model serializer
    """
    user = UserSummarySerializer()
    user_score = serializers.IntegerField(source='get_user_score')
    media = PostMediaSerializer(source='media_files', many=True) # media _set

    class Meta:
        model = Post
        fields = [
            'uuid',
            'created_at',
            'content',
            'likes_count',
            'user',
            'user_score',
            'media'
        ]
