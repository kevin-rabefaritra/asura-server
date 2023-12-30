from rest_framework import mixins, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from asura.auth import TokenAuthentication
from asura.models import Post
from asura.serializers.post_serializer import PostSerializer
from asura.exceptions.generic_exceptions import MissingParametersException
from asura.services import post_services

class PostList(mixins.ListModelMixin, generics.GenericAPIView):
    """
    API view for retrieving posts
    """
    authentication_classes = [TokenAuthentication]

    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    # Todo: add pagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostCreate(APIView):
    '''
    Used to publish a Post
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        '''
        @param request, requires the following value:
        - content {string} the content of the Post
        '''
        data = request.data
        try:
            if 'content' not in data:
                raise MissingParametersException(['content'])
            
            post_services.save(request.user, data['content'])
            return Response(status=status.HTTP_201_CREATED)

        except MissingParametersException as e:
            print('[PostCreate] %s' % e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
