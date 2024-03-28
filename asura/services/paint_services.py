
from asura.models import Post
from PIL import Image, ImageFont, ImageDraw

def draw_post(post: Post):
    """
    Generates a visual representation of a Post object
    """
    result = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(result)
    draw.text((16, 16), post.content)
    return result
