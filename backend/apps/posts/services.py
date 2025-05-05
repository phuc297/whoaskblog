from .models import Post, Comment, PostVote

def get_published_posts():
    return Post.objects.filter(status='published').order_by('-created_at')

def get_draft_posts(author):
    return Post.objects.filter(author=author).order_by('-created_at')
    