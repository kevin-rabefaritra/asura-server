from asura.models import User, Post

def save(user: User, content: str) -> Post or None:
    """
    Creates and save a Post object
    """
    post = Post(content=content, user=user)
    post.save()
    return post

def find_by_keyword(keyword: str) -> list:
    """
    Find all posts with the provided keyword
    """
    return Post.objects.filter(content__icontains=keyword)