from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from asura.auth import TokenAuthentication
from asura.models import Conversation, Message, UserConversation
from asura.serializers.messages_serializer import MessageSerializer
from asura.services import conversation_services, message_services


class MessageSend(APIView):
    """
    API endpoint used to send a message
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Creates a Message object.
        If there is no Conversation, it will be created.
        [Dev]: sender uuid is provided
        [Prod]: sender uuid is obtained from token
        :param request:
            - content: plain text of the message content (v0.1)
            - (dev only) sender: uuid of the sending User
            - content_type: type of the content (refer to MessageType keys)
            - conversation: uuid of the Conversation
             OR
            - recipient: uuid of the User (if the Conversation is not created yet)
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        try:
            if 'recipient' in data:
                # recipient has been explicitly provided
                # we create a conversation (if there is none between the two users)
                conversation = conversation_services.find_or_create(
                    sender_uuid=request.user.uuid,
                    recipient_uuid=data['recipient'],
                    conversation_type=Conversation.ConversationType.INDIVIDUAL
                )
                data['conversation'] = conversation.uuid

            # create the message in the conversation
            message_services.save(
                conversation_uuid=data['conversation'],
                sender_uuid=request.user.uuid,
                content=data['content'],
                message_type=data['content_type']
            )
            return Response(data=None, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MessageList(mixins.ListModelMixin, generics.GenericAPIView):
    """
    API endpoint to list messages in a conversation
    We identify the user token to check if they have access to the conversation
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, uuid, *args, **kwargs):
        # We check that the user is part of the conversation
        user = request.user
        if conversation_services.is_user_in_conversation(uuid, user.uuid):
            return self.list(request, *args, **kwargs)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        queryset = super(MessageList, self).get_queryset()
        queryset = queryset.filter(conversation__uuid=self.kwargs['uuid'])
        queryset = queryset.order_by('-updated_at')
        return queryset
