from rest_framework import serializers

from asura.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a serializer for User
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'email', 'password', 'bio', 'birthday']


class UserBatchSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a serializer for Users in batch (read purposes only)
    """

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'bio']