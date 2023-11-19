from asura.exceptions.conversation_exceptions import ConversationNotFoundException
from asura.exceptions.user_exceptions import UserNotFoundException
from asura.models import Message
from asura.services import conversation_services, user_services


def save(conversation_uuid, sender_uuid, content, message_type) -> Message or None:
    """
    Creates a Message entry
    :param sender_uuid:
    :param conversation_uuid:
    :param content:
    :param message_type:
    :return:
    :raises UserNotFoundException
    """
    sender = user_services.find_by_uuid(sender_uuid, raise_exception_if_not_found=True)
    conversation = conversation_services.find_by_uuid(
        conversation_uuid,
        raise_exception_if_not_found=True
    )
    message = Message(
        conversation=conversation,
        user=sender,
        content=content,
        type=message_type
    )
    message.save()
    return message
