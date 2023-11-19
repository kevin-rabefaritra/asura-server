from django.contrib import admin

# Register your models here.
from asura.models import User, Message, Conversation, UserConversation

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(UserConversation)
