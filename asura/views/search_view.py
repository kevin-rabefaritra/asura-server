from rest_framework.views import APIView
from asura.auth import TokenAuthentication
from asura.models import User
from rest_framework import status
from rest_framework.response import Response
from asura.services import user_services, post_services

from asura.serializers.users_serializer import UserSerializer, UserBatchSerializer
from asura.serializers.post_serializer import PostSerializer

class ContentSearch(APIView):
    """
    API endpoint for searching content (User + Post)
    Token is not required but optional
    Response example:
    - 200: 
    """
    authentication_classes = [TokenAuthentication]

    MIN_KEYWORD_LENGTH = 3

    def get(self, request, keyword: str):
        keyword = keyword.strip()
        if len(keyword) >= self.MIN_KEYWORD_LENGTH:
            users = user_services.find_by_keyword(keyword)
            posts = post_services.find_by_keyword(keyword)
            user_serializer = UserBatchSerializer(users, many=True)
            post_serializer = PostSerializer(posts, many=True)

            data = {
                'total': len(users) + len(posts),
                'results': {
                    'users': user_serializer.data,
                    'posts': post_serializer.data
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data=[], status=status.HTTP_200_OK)
