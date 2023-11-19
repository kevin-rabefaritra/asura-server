from django.urls import path
from django.urls import include
from rest_framework import routers

from asura.views import user_view
from asura.views.conversation_view import ConversationList
from asura.views.message_view import MessageSend, MessageList
from asura.views.token_view import TokenIdentification, TokenRenewal
from asura.views.user_view import UserList, UserSignIn, UserSearch, \
    UserBasicInfo, \
    UserUpdatePassword

urlpatterns = [
    path('hello/', user_view.hello),

    # Users
    path('users/', UserList.as_view()),
    path('users/signin', UserSignIn.as_view()),
    path('users/search/<str:keyword>', UserSearch.as_view()),

    path('users/profile/basic', UserBasicInfo.as_view()),
    path('users/profile/basic/<str:uuid>', UserBasicInfo.as_view()),
    path('users/password/update', UserUpdatePassword.as_view()),

    # Message
    path('message/send', MessageSend.as_view()),

    # Conversation
    path('conversations/', ConversationList.as_view()),
    path('messages/<str:uuid>', MessageList.as_view()),

    # Token
    path('token/identify/<str:key>', TokenIdentification.as_view()),
    path('token/renew', TokenRenewal.as_view()),

    path('api-auth/', include('rest_framework.urls')),
]
