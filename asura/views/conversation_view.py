
from rest_framework import mixins, generics

from asura.auth import TokenAuthentication
from asura.models import Conversation
from asura.serializers.conversations_serializer import ConversationSerializer
from rest_framework.permissions import IsAuthenticated

from asura.services import conversation_services


class ConversationList(mixins.ListModelMixin, generics.GenericAPIView):
    """
    API endpoint for listing Conversations
    We only list conversation involving the token owner
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Conversation.objects.all().order_by('-updated_at')
    serializer_class = ConversationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns the queryset
        :return:
        """
        queryset = super().get_queryset()

        # we get the token owner (we search using the ID to avoid additional table JOIN with UUID).
        user = self.request.user
        queryset = queryset.filter(users__user=user.id)
        return queryset
