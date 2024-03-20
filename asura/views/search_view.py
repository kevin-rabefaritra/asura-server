from rest_framework.views import APIView
from asura.auth import TokenAuthentication
from asura.models import User
from rest_framework import status
from rest_framework.response import Response
from asura.services import user_services, post_services
from django.core.paginator import Paginator
from re import fullmatch, search

from asura.serializers.users_serializer import UserSerializer, \
    UserBatchSerializer
from asura.serializers.post_serializer import PostSerializer

class ContentSearch(APIView):
    """
    API endpoint for searching content (User + Post)
    
    Usage:
    - `/keyword` (default)
    Will look for all users and posts (content) having the keyword

    - `/posts:{username}`
    Will look for all posts published by a specific user
    
    Notes:
    Token is not required but can be provided

    Response example:
    - 200: 
    """
    authentication_classes = [TokenAuthentication]

    MIN_KEYWORD_LENGTH = 3
    MAX_RESULTS = 20

    def get(self, request, keyword: str):
        keyword = keyword.strip()
        page = request.GET.get('page', 1)
        user = request.user

        if len(keyword) >= self.MIN_KEYWORD_LENGTH:
            if user.is_authenticated:
                # may want to do something if the user is authenticated
                pass

            users = None
            posts = None

            if fullmatch(r'posts:[a-zA-Z0-9\-\_]+', keyword):
                # Extract the username from the search input
                _search = search(r'posts:([a-zA-Z0-9\-\_]+)', keyword)
                username = _search.groups()[0]

                # Retrieve posts with the username
                posts = post_services.find_by_username(username)
            else:
                # default search
                users = user_services.find_by_keyword(keyword)
                posts = post_services.find_by_keyword(keyword)
            
            # Merge objects in one list
            objects = [e for e in UserBatchSerializer(users, many=True, context={'request': request}).data]
            objects += [e for e in PostSerializer(posts, many=True).data]

            # Create a paginator
            paginator = Paginator(objects, self.MAX_RESULTS).page(page)
            data = {
                'total': len(paginator.object_list),
                'results': paginator.object_list,
                'next_page': paginator.next_page_number() if paginator.has_next()
                    else None
            }
        else:
            data = []
        return Response(data=data, status=status.HTTP_200_OK)
