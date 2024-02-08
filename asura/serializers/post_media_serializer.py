from rest_framework import serializers
from asura.models import PostMedia

class PostMediaSerializer(serializers.ModelSerializer):
    """
    Represents a PostMedia model serializer
    """

    class Meta:
        model = PostMedia
        fields = ['file', 'alt']
