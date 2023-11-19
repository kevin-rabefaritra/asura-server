
class ConversationNotFoundException(Exception):
    """
    Thrown when a conversation is not found
    """
    def __init__(self, message='Conversation not found'):
        super().__init__(message)


class OperationNotPermittedException(Exception):
    """
    Thrown when an operation is not permitted.
    """
    def __init__(self, message='This operation is not permitted'):
        super().__init__(message)