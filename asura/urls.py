from django.urls import path
from django.urls import include
from rest_framework import routers

from asura.views import user_view
from asura.views.conversation_view import ConversationList
from asura.views.message_view import MessageSend, MessageList
from asura.views.token_view import TokenIdentification, TokenRenewal
from asura.views.user_view import UserList, UserSignIn, \
    UserBasicInfo, \
    UserUpdatePassword
from asura.views.post_view import PostList, PostCreate, PostReact
from asura.views.search_view import ContentSearch

urlpatterns = [

    # General
    path('hello/', user_view.hello),
    path('search/<str:keyword>', ContentSearch.as_view()),

    # Users
    path('users/', UserList.as_view()),
    path('users/signin', UserSignIn.as_view()),

    path('users/profile/basic', UserBasicInfo.as_view()),
    path('users/profile/basic/<str:uuid>', UserBasicInfo.as_view()),
    path('users/password/update', UserUpdatePassword.as_view()),

    # Message
    path('message/send', MessageSend.as_view()),

    # Conversation
    path('conversations/', ConversationList.as_view()),
    path('messages/<str:uuid>', MessageList.as_view()),

    # Post
    path('posts/', PostList.as_view()),
    path('posts/create', PostCreate.as_view()),
    path('posts/react/<str:uuid>', PostReact.as_view()),

    # Token
    path('token/identify/<str:key>', TokenIdentification.as_view()),
    path('token/renew', TokenRenewal.as_view()),

    path('api-auth/', include('rest_framework.urls')),
]
