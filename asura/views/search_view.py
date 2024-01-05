from rest_framework.views import APIView
from asura.auth import TokenAuthentication
from asura.models import User
from rest_framework import status
from rest_framework.response import Response
from asura.services import user_services, post_services
from django.core.paginator import Paginator

from asura.serializers.users_serializer import UserSerializer, UserBatchSerializer
from asura.serializers.post_serializer import PostSerializer

class ContentSearch(APIView):
    """
    API endpoint for searching content (User + Post)
    Token is not required but can be provided
    Response example:
    - 200: 
    """
    authentication_classes = [TokenAuthentication]

    MIN_KEYWORD_LENGTH = 3
    MAX_RESULTS = 50

    def get(self, request, keyword: str):
        keyword = keyword.strip()
        page = request.GET.get('page', 1)
        user = request.user

        if len(keyword) >= self.MIN_KEYWORD_LENGTH:
            if user.is_authenticated:
                # may want to do something if the user is authenticated
                pass

            users = user_services.find_by_keyword(keyword)[:self.MAX_RESULTS]
            posts = post_services.find_by_keyword(keyword)[:self.MAX_RESULTS]
            objects = UserBatchSerializer(users, many=True).data + PostSerializer(posts, many=True).data

            # Create a paginator
            paginator = Paginator(objects, self.MAX_RESULTS).page(page)
            data = {
                'total': len(paginator.object_list),
                'results': paginator.object_list,
                'has_next': paginator.has_next()
            }
        else:
            data = []
        return Response(data=data, status=status.HTTP_200_OK)
