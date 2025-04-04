from django.shortcuts import render

from posts.models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, 'layout/index.html', context={'posts': posts})

def test(request):
    return render(request, 'test/test.html')
