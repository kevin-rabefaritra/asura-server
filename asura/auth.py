from rest_framework import authentication

from asura.services import token_services
from rest_framework.exceptions import AuthenticationFailed
from asura.models import Token


class TokenAuthentication(authentication.BasicAuthentication):

    TOKEN_LENGTH = 40

    """
    Custom token authentication
    """
    def authenticate(self, request):
        """
        Used for token authentication
        :param request:
        :return:
        """
        # read authentication header
        authorization = request.headers.get('Authorization')
        if authorization is not None and len(authorization.split()) > 1:
            # Split in 2
            _, key = authorization.split(' ', 1)
            token = token_services.find_by_key(key, type=Token.TokenType.ACCESS)

            if token is not None and not token_services.has_expired(token):
                # Second None argument is required by parent class' method
                return (token.user, None)
            else:
                raise AuthenticationFailed('Provided auth. is not valid.')
        else:
            return None
