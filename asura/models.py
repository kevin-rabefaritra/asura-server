import binascii
import os

from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid
import datetime

from asura.helpers import date_time_helper
from kianjafacea import settings


class User(models.Model):
    """
    Represents a messaging user
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=64, unique=True)
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=256)
    bio = models.CharField(max_length=1024, null=True, default=None)
    birthday = models.DateField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    def is_authenticated(self):
        """
        Required by custom authentication TokenAuthentication
        :return:
        """
        return True


class Conversation(models.Model):
    """
    Represents a conversation instance (individual or group)
    """
    class ConversationType(models.TextChoices):
        INDIVIDUAL = "individual", _('Individual')
        GROUP = "group", _('Group')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=50, choices=ConversationType.choices, default=ConversationType.INDIVIDUAL)


class UserConversation(models.Model):
    """
    Represents a User relationship to a Conversation
    Many to many
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    conversation = models.ForeignKey(to=Conversation, on_delete=models.SET_NULL, null=True, related_name='user_conversations')


class Message(models.Model):
    """
    Represents a message object
    """
    class MessageType(models.TextChoices):
        TEXT = "text", _('Plain text')
        AUDIO = "audio", _('Audio')
        GIF = "gif", _('Gif')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    conversation = models.ForeignKey(to=Conversation, on_delete=models.SET_NULL, null=True, related_name='conversation_messages')
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, default=None)
    content = models.JSONField(default=dict, null=True)
    type = models.CharField(max_length=50, choices=MessageType.choices, default=MessageType.TEXT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Token(models.Model):
    """
    The default authorization token model (used with Asura.User)
    """
    class TokenType(models.TextChoices):
        ACCESS = "access", _('Access token')
        REFRESH = "refresh", _('Refresh token')

    key = models.CharField(_("Key"), max_length=1000, primary_key=True)
    user = models.ForeignKey(
        User, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    type = models.CharField(_("Type"), max_length=20, choices=TokenType.choices, default=TokenType.ACCESS)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(self.type)
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls, type):
        token_length = settings.ACCESS_TOKEN_LENGTH
        if type == Token.TokenType.REFRESH:
            token_length = settings.REFRESH_TOKEN_LENGTH
        return binascii.hexlify(os.urandom(token_length)).decode()

    def __str__(self):
        return self.key


class Post(models.Model):
    """
    Represents a timeline post
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    content = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='posts')

    # Denormalized fields
    likes_count = models.PositiveIntegerField()
    comments_count = models.PositiveIntegerField()


class PostLike(models.Model):
    """
    Represents a post like
    """
    score = models.PositiveSmallIntegerField(default=1)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(to=Post, on_delete=models.SET_NULL, related_name='post_likes')


class PostMedia(models.Model):
    """
    Represents a media file attached to a Post
    """
    file = models.FileField(upload_to='posts/')
    post = models.ForeignKey(to=Post, on_delete=models.SET_NULL, related_name='media_files')

