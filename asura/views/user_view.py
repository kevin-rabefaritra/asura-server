from asura.auth import TokenAuthentication
from asura.models import User
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from asura.serializers.users_serializer import UserSerializer, UserBatchSerializer
from asura.exceptions.user_exceptions import UserNotFoundException
from asura.exceptions.generic_exceptions import MissingParametersException
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView

from asura.services import token_services, user_services
from asura.models import Token


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
            access_token = token_services.get(user, type=Token.TokenType.ACCESS, create_if_none=True)
            refresh_token = token_services.get(user, type=Token.TokenType.REFRESH, create_if_none=True)
            serializer = UserSerializer(user, context={'request': request})
            response = {
                'user': serializer.data,
                'token': access_token.key,
                'refreshToken': refresh_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
        - oldPassword: old user password
        - newPassword: new user password
        
        :note
        - user is identified by token authentication
        - password confirmation is performed on client side
        """
        # check that both parameters are provided
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')
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

    def get(self, request, uuid: str = None):
        """
        GET request to show a user's basic info
        
        1) if :uuid parameter is provided, we fetch the user's basic info
        2) if not, we retrieve the user from the token
        """
        try:
            user = request.user
            if uuid is None and not user.is_authenticated:
                # UUID is not provided and user is not authenticated
                # The user session may have expired
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            _uuid = uuid or request.user.uuid
            
            user = user_services.find_by_uuid(_uuid)

            # When passing the request to a serializer, absolute URLs are built
            # https://stackoverflow.com/a/65139515
            serializer = UserSerializer(user, context={'request': request})
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


class UserUpdatePhoto(APIView):
    """
    API for updating a user profile picture (POST only)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        The request body must have the following structure.
        {
            "media": "data:<data type>;base64,<data>"
        }
        """
        data = request.data
        user_uuid = request.user.uuid
        try:
            if 'media' not in data:
                raise MissingParametersException('media')
            
            if data['media'] is None:
                user_services.remove_photo(user_uuid)
            else:            
                user_services.update_photo(data['media'], user_uuid)
            return Response(status=status.HTTP_201_CREATED)
        
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        except MissingParametersException:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except UserNotFoundException:
            return Response(status=status.HTTP_404_NOT_FOUND)

def hello(request):
    """
    Returns hello
    :param request:
    :return:
    """
    return JsonResponse(data={'response': 'hello'})
