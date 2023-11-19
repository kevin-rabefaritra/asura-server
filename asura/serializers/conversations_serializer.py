from asura.models import Conversation
from rest_framework import serializers


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a serializer for a Conversation
    """
    class Meta:
        model = Conversation
        fields = ['uuid', 'name', 'type', 'updated_at']
