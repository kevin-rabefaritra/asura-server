from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from asura.auth import TokenAuthentication
from asura.serializers.users_serializer import UserSerializer
from asura.services import token_services
from asura.models import Token


class TokenIdentification(APIView):
    """
    API endpoint for checking a token owner
    Note: this only works with access tokens
    """

    def get(self, request, key: str) -> Response:
        token = token_services.find_by_key(key=key, type=Token.TokenType.ACCESS)

        if token is not None and token.user is not None:
            user = token.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class TokenRenewal(APIView):
    """
    API endpoint to renew an expired token.
    Note:
    - A refresh token is required. Otherwise the API returns 401.
    - The expired access token must be provided.

    (1) Request header must contain:
    Authorization: Basic [ACCESS_TOKEN]

    (2) Request body must contain:
    "refreshToken": [REFRESH_TOKEN]

    Returns 401 if:
    (1) any token is missing
    (2) the refreshToken is expired
    (3) the access token and the refresh token don't belong to the same user
    
    Returns 404 if a token doesn't belong to any user
    """

    authentication_classes = [TokenAuthentication]

    def post(self, request) -> Response:
        """
        :param request:
        Contains the token in its header
        :return:
        """
        authorization = request.headers.get('Authorization')
        refresh_token = request.data.get('refreshToken')

        if authorization is None or refresh_token is None:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        
        # Extract access and refresh token
        _, key = authorization.split()
        access_token = token_services.find_by_key(key, type=Token.TokenType.ACCESS)
        refresh_token = token_services.find_by_key(refresh_token, type=Token.TokenType.REFRESH)

        # Check that both tokens exist AND belong to the same user
        if access_token is not None and refresh_token is not None:
            # Check that the refresh token has not expired
            if not token_services.has_expired(refresh_token) and access_token.user == refresh_token.user:
                new_token = token_services.generate(
                    access_token.user,
                    Token.TokenType.ACCESS,
                    invalidate_existing=True
                )
                data = {'token': new_token.key}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
