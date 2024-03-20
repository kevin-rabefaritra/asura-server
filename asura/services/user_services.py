from asura.exceptions.user_exceptions import UserNotFoundException
from asura.models import User
from asura.helpers import media_helper
from asura.helpers import string_helper


def find_by_uuid(uuid: str, raise_exception_if_not_found: bool = True) -> User or None:
    """
    Returns a User based on their uuid
    :param raise_exception_if_not_found: 
    :param uuid:
    :return: the User or None
    :throws
    - ValidationError, UserNotFoundException
    """
    result = User.objects.filter(uuid=uuid).first()
    if result is None and raise_exception_if_not_found:
        raise UserNotFoundException('User UUID %s not found' % uuid)
    else:
        return result
    
def find_by_username(username: str, raise_exception_if_not_found: bool = True) -> User or None:
    """
    Returns a User based on their username
    """
    result = User.objects.filter(username=username).first()
    if result is None and raise_exception_if_not_found:
        raise UserNotFoundException('User USERNAME %s not found' % username)
    else:
        return result


def find_by_username_password(username: str, password: str) -> User or None:
    """
    Returns a user based on their username / password
    :param username:
    :param password:
    :return:
    """
    if username is not None and password is not None:
        return User.objects.filter(username=username, password=password).first()
    else:
        return None

def find_by_keyword(keyword: str) -> list:
    """
    Find all users with the provided keyword
    """
    return User.objects.filter(username__icontains=keyword)


def update_password(username: str, old_password: str, new_password) -> bool:
    """
    Updates a user password
    :param username
    :param old_password
    :param new_password
    :return
    true if operation completed successfully
    false otherwise
    """
    user = find_by_username_password(username, old_password)
    if user is not None:
        user.password = new_password
        user.save()
        return True
    else:
        raise UserNotFoundException('User / password combination not found')


def update_basic_info(uuid: str, bio: str, birthday: str) -> bool:
    """
    Updates a user basic info
    - bio
    - birthday
    """
    user = find_by_uuid(uuid)
    if user is not None:
        user.bio = bio or None
        user.birthday = birthday
        user.save()
        return True
    else:
        raise UserNotFoundException()
    

def update_photo(media: str, user_uuid: str) -> bool:
    """
    Updates the profile picture of a user
    """
    user = find_by_uuid(user_uuid)
    if user is not None:
        filename = string_helper.generate_hex_uuid()
        file_content = media_helper.base64_to_file_content(media, filename)
        user.profile_picture = file_content
        user.save()
        return True
    else:
        raise UserNotFoundException()


def remove_photo(user_uuid: str) -> bool:
    """
    Removes the profile picture of a user
    """
    user = find_by_uuid(user_uuid)
    if user is not None:
        user.profile_picture = None
        user.save()
        return True
    else:
        raise UserNotFoundException()