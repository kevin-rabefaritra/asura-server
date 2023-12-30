import datetime

from asura.helpers import date_time_helper
from asura.models import User, Token
from kianjafacea import settings


def get(user: User, type: str=Token.TokenType.ACCESS, create_if_none=True) -> Token or None:
    """
    Returns the last valid token for the user or creates and returns a new one
    :param create_if_none:
    :param user:
    :return:
    """
    now = date_time_helper.now()
    token_lifespan = get_token_lifespan(type)
    min_created_at = now - datetime.timedelta(seconds=token_lifespan)

    token = Token.objects.filter(user=user, type=type, created_at__gt=min_created_at).first()
    if token is None and create_if_none:
        token = generate(user, type, invalidate_existing=False)
    return token


def find_by_key(key: str, type) -> Token or None:
    """
    Returns a token based on its key and type
    :param key:
    :param type:
    :return:
    """
    return Token.objects.filter(key=key, type=type).first()


def has_expired(token: Token) -> bool:
    """
    Returns true if a token has expired
    :param token:
    :return:
    """
    now = date_time_helper.now()
    expiration_duration = get_token_lifespan(token.type)
    min_datetime = now - datetime.timedelta(seconds=expiration_duration)
    return token.created_at <= min_datetime


def get_token_lifespan(type: str) -> int:
    """
    Returns a token lifespan (in seconds) depending on its type
    """
    if type == Token.TokenType.ACCESS:
        return settings.ACCESS_TOKEN_EXPIRED_AFTER_SECONDS
    else:
        return settings.REFRESH_TOKEN_EXPIRED_AFTER_SECONDS


def generate(user: User, type: str=Token.TokenType.ACCESS, invalidate_existing=False) -> Token:
    """
    Creates a new token for the user
    :param type:
    the token type (access or refresh)
    :param invalidate_existing:
    if True, all existing tokens associated with the user will be invalidated
    :param user:
    :return:
    """
    if invalidate_existing:
        Token.objects.filter(user=user, type=type).delete()

    return Token.objects.create(user=user, type=type)
