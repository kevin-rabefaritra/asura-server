import datetime

from asura.helpers import date_time_helper
from asura.models import User, Token
from kianjafacea import settings


def get(user: User, create_if_none=True) -> Token or None:
    """
    Returns the last valid token for the user or creates and returns a new one
    :param create_if_none:
    :param user:
    :return:
    """
    now = date_time_helper.now()
    min_created_at = now - datetime.timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)

    token = Token.objects.filter(user=user, created__gt=min_created_at).first()
    if token is None and create_if_none:
        token = generate(user, invalidate_existing=False)
    return token


def find_by_key(key: str) -> Token or None:
    """
    Returns a token based on its key
    :param key:
    :return:
    """
    return Token.objects.filter(key=key).first()


def has_expired(token: Token) -> bool:
    """
    Returns true if a token has expired
    :param token:
    :return:
    """
    now = date_time_helper.now()
    min_datetime = now - datetime.timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
    return token.created <= min_datetime


def generate(user: User, invalidate_existing=False) -> Token:
    """
    Creates a new token for the user
    :param invalidate_existing:
    if True, all existing tokens associated with the user will be invalidated
    :param user:
    :return:
    """
    if invalidate_existing:
        Token.objects.filter(user=user).delete()

    return Token.objects.create(user=user)
