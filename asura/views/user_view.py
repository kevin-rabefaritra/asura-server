from asura.auth import TokenAuthentication
from asura.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from asura.serializers.users_serializer import UserSerializer, UserBatchSerializer
from asura.exceptions.user_exceptions import UserNotFoundException
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView

from asura.services import token_services, user_services


class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    API endpoint for Users to be listed / created
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    """
    GET: List users
    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    """
    POST: Sign-up - Create single user
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserSignIn(mixins.ListModelMixin, generics.GenericAPIView):
    """
    API endpoint for a single user to sign in
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = user_services.find_by_username_password(request.data.get('username'), request.data.get('password'))
        if user is not None:
            token = token_services.get(user, create_if_none=True)
            serializer = UserSerializer(user)
            response = {
                'user': serializer.data,
                'token': token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserSearch(APIView):
    """
    API endpoint for searching users
    Response example:
    - 200: 
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    MIN_KEYWORD_LENGTH = 3

    def get(self, request, keyword: str):
        keyword = keyword.strip()
        if len(keyword) >= self.MIN_KEYWORD_LENGTH:
            users = User.objects.filter(username__icontains=keyword)
            serializer = UserBatchSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=[], status=status.HTTP_200_OK)
        

class UserUpdatePassword(APIView):
    """
    API endpoint for updating a single user password
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        POST request to update a user's password
        :params request contains:
        - old_password: old user password
        - new_password: new user password
        
        :note
        - user is identified by token authentication
        - password confirmation is performed on client side
        """
        # check that both parameters are provided
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if old_password is not None and new_password is not None:
            try:
                username = request.user.username
                user_services.update_password(username, old_password, new_password)
                return Response(status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserBasicInfo(APIView):
    """
    GET - Shows a user's basic info
    POST - Updates a user's basic info (bio, birthday)
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GET request to show a user's basic info
        
        1) if :uuid parameter is provided, we fetch the user's basic info
        2) if not, we retrieve the user from the token
        """
        try:
            # default is token user
            uuid = request.user.uuid
            if 'uuid' in kwargs:
                uuid = kwargs['uuid']
            
            user = user_services.find_by_uuid(uuid)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except (UserNotFoundException, ValidationError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        POST request to update a user's basic info
        :params request contains:
        - bio: user's bio
        - birthday: user's birthday
        
        :note
        - user is identified by token authentication
        """
        # check that both parameters are provided
        bio = request.data.get('bio')
        birthday = request.data.get('birthday')

        try:
            uuid = request.user.uuid
            user_services.update_basic_info(uuid, bio, birthday)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def hello(request):
    """
    Returns hello
    :param request:
    :return:
    """
    return JsonResponse(data={'response': 'hello'})
