from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from asura.auth import TokenAuthentication
from asura.serializers.users_serializer import UserSerializer
from asura.services import token_services


class TokenIdentification(APIView):
    """
    API endpoint for checking a token owner
    """

    def get(self, request, key: str) -> Response:
        token = token_services.find_by_key(key=key)

        if token is not None and token.user is not None:
            user = token.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class TokenRenewal(APIView):
    """
    API endpoint to renew an expired token
    Returns 401 if the token is missing.
    Returns 404 if the token doesn't belong to any user
    """

    def get(self, request) -> Response:
        """
        :param request:
        Contains the token in its header
        :return:
        """
        authorization = request.headers.get('Authorization')
        if authorization is not None:
            _, key = authorization.split()
            token = token_services.find_by_key(key)
            if token is not None:
                new_token = token_services.generate(token.user)

                data = {'token': new_token.key}
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(None, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
