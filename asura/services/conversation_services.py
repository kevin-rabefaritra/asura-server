from asura.exceptions.conversation_exceptions import ConversationNotFoundException, OperationNotPermittedException
from asura.models import Conversation, UserConversation
from asura.services import user_services


def save(sender_uuid, recipient_uuid, conversation_type) -> Conversation:
    """
    Creates a conversation
    Also creates two entries of UserConversation to include both sender and recipient
    :param conversation_type:
    :param sender_uuid:
    :param recipient_uuid:
    :param type:
    :return:
    """
    # Create the Conversation entry
    conversation = Conversation()
    conversation.name = 'default'
    conversation.type = conversation_type
    conversation.save()

    # Create two UserConversation entries
    sender = user_services.find_by_uuid(sender_uuid)
    recipient = user_services.find_by_uuid(recipient_uuid)

    UserConversation(user=sender, conversation=conversation).save()
    UserConversation(user=recipient, conversation=conversation).save()
    return conversation


def find_by_uuid(uuid: str, raise_exception_if_not_found: bool = True) -> Conversation or None:
    """
    Returns a Conversation based on its UUID
    :param raise_exception_if_not_found:
    :param uuid:
    :return:
    :raises ConversationNotFoundException
    """
    result = Conversation.objects.filter(uuid=uuid).first()
    if result is None and raise_exception_if_not_found:
        raise ConversationNotFoundException('Conversation UUID %s not found' % uuid)
    else:
        return result


def find_or_create(sender_uuid, recipient_uuid, conversation_type) -> Conversation:
    """
    Finds a Conversation between the two users
    If there is none, create the Conversation entry.
    SQL equivalent:
        SELECT c.*
        FROM Conversation c
        JOIN UserConversation uc1 ON c.conversation_id = uc1.conversation_id
        JOIN UserConversation uc2 ON c.conversation_id = uc2.conversation_id
        WHERE uc1.user_id = 'UserA_ID' AND uc2.user_id = 'UserB_ID';

    In this query, we are joining the Conversation table with the
    UserConversation table twice, once for User A (uc1) and once for
    User B (uc2). We then specify the user IDs for User A and User B in the
    WHERE clause to filter the conversations that have both users.

    In this code snippet,
    - you retrieve the user objects for User A and User B using their IDs
    - you perform a query on the Conversation model by filtering the
    conversations based on the userconversation__user field, which refers to
    the related User objects through the intermediary table.

    :param sender_uuid:
    :param recipient_uuid:
    :param conversation_type:
    :return:
    :raises OperationNotPermittedException
    """
    if sender_uuid == recipient_uuid:
        raise OperationNotPermittedException('Sender and recipient cannot be the same user.')

    user_a = user_services.find_by_uuid(sender_uuid, raise_exception_if_not_found=True)
    user_b = user_services.find_by_uuid(recipient_uuid, raise_exception_if_not_found=True)
    conversation = Conversation.objects\
        .filter(type=conversation_type)\
        .filter(userconversation__user=user_a)\
        .filter(userconversation__user=user_b)\
        .first()
    if conversation is None:
        conversation = save(sender_uuid, recipient_uuid, conversation_type)
    return conversation


def find_all_including_user(user_uuid: str) -> list:
    """
    Returns all conversation involving a user
    :param user_uuid:
    :return:
    """
    return UserConversation.objects.filter(user__uuid=user_uuid)


def is_user_in_conversation(conversation_uuid: str, user_uuid: str) -> bool:
    """
    Returns True if the user is part of the conversation, else False
    :param conversation_uuid: the UUID of the conversation
    :param user_uuid: the UUID of the user
    """
    user_conversation = UserConversation.objects.filter(
        conversation__uuid=conversation_uuid,
        user__uuid=user_uuid
    ).first()
    return user_conversation is not None
