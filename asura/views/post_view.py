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

    serializer_class = PostSerializer

    # Page size is defined in settings.py

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Fetch Posts and for each Post, add an additional field "user_score" to
        represent the score given by the user
        """
        posts = Post.objects.all().order_by('-created_at')

        # if the user is Anonymous, we can return the Post list right away
        if not self.request.user.is_authenticated:
            pass
        else:
            # user is authenticated, we fetch the posts reactions for the
            # selected posts
            user_uuid = self.request.user.uuid
            post_uuids = [_post.uuid for _post in posts]
            post_reactions = post_services.find_reactions(user_uuid, post_uuids)
            
            # bind PostReaction to Post list
            for post in posts:
                post_reaction = list(filter(lambda x:x.post.uuid == post.uuid, post_reactions))
                if post_reaction:
                    post.user_score = post_reaction[0].score

        return posts


class PostCreate(APIView):
    """
    Used to publish a Post
    """
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


class PostReact(APIView):
    """
    Used to react to a Post
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid: str):
        '''
        @param request, requires the following value:
        - score {int} the updated score -1;1;0
        @param uuid the identifier of the Post
        '''
        data = request.data
        try:
            if 'score' not in data:
                raise MissingParametersException(['score'])
            
            post_services.add_reaction(request.user, uuid, data['score'])
            return Response(status=status.HTTP_201_CREATED)

        except MissingParametersException as e:
            print('[PostReact] %s' % e)
            return Response(status=status.HTTP_400_BAD_REQUEST)