from rest_framework import serializers

from asura.models import Message


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Message
    """
    user_uuid = serializers.CharField(source='user.uuid')
    conversation_uuid = serializers.CharField(source='conversation.uuid')

    class Meta:
        model = Message
        fields = ['uuid', 'content', 'user_uuid', 'conversation_uuid', 'created_at', 'updated_at', 'type']
