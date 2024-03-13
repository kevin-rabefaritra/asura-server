from rest_framework import serializers

from asura.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
    Represents a serializer for User
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'email',
                  'password', 'bio', 'birthday', 'profile_picture', 'created_at']


class UserBatchSerializer(serializers.HyperlinkedModelSerializer):
    """
    Represents a serializer for Users in batch (read purposes only)
    """

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'bio',
                  'profile_picture']
        

class UserSummarySerializer(serializers.ModelSerializer):
    """
    Simplified User serializer
    """
    class Meta:
        model = User 
        fields = ['uuid', 'first_name', 'last_name', 'username', 'profile_picture']