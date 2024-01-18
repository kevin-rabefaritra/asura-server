from asura.models import User, Post, PostReaction

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


def find_by_uuid(uuid: str) -> Post or None:
    """
    Returns a Post given its uuid
    """
    return Post.objects.filter(uuid=uuid).first()


def add_reaction(user: User, uuid: str, score: int, update_post: bool=True):
    """
    Creates or update a Post reaction
    @params
    - user: the User instance
    - uuid: the uuid of the Post
    - score: the score to apply
    - update_post: if True, updates the Post score
    """
    post = find_by_uuid(uuid)
    post_reaction = PostReaction.objects.filter(
        post__uuid=uuid,
        user__uuid=user.uuid
    ).first()

    if score == post_reaction.score:
        # There are no changes
        return
    
    # make sure the score is between [-1;1]
    score = 1 if score > 1 else -1 if score < -1 else score
    
    if post_reaction is None:
        post.likes_count += score

        # Create a PostReaction
        post_reaction = PostReaction()
        post_reaction.score = score
        post_reaction.post = post
        post_reaction.user = user
    else:
        # We deduct the previous reaction and add the new one
        post.likes_count = post.likes_count - post_reaction.score + score

        # Update existing PostReaction
        post_reaction.score = score

    if update_post:
        post.save()
    
    post_reaction.save()
