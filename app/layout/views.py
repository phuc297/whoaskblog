from django.shortcuts import render

from posts.models import Post


def index(request):
    posts = Post.objects.all()
    for post in posts:
        post.comments_count = post.comments.count()
        post.description = post.content[:60] + '...'
        post.category_color = post.category.color
    return render(request, 'layout/index.html', context={'posts': posts})

def test(request):
    return render(request, 'test/test.html')
