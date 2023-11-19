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
    last_name = models.CharField(max_length=50)
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
    conversation = models.ForeignKey(to=Conversation, on_delete=models.SET_NULL, null=True, related_name='users')


class Message(models.Model):
    """
    Represents a message object
    """
    class MessageType(models.TextChoices):
        TEXT = "text", _('Plain text')
        AUDIO = "audio", _('Audio')
        GIF = "gif", _('Gif')

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    conversation = models.ForeignKey(to=Conversation, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, default=None)
    content = models.JSONField(default=dict, null=True)
    type = models.TextField(max_length=50, choices=MessageType.choices, default=MessageType.TEXT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Token(models.Model):
    """
    The default authorization token model (used with Asura.User)
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(
        User, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

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
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
