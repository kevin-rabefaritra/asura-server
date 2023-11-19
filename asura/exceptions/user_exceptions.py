
class UserNotFoundException(Exception):
    """
    Thrown when a User does not exist
    """
    def __init__(self, message='User not found'):
        super().__init__(message)
