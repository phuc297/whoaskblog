from django.shortcuts import render

from posts.models import Post
from users.models import Profile


def index(request):
    posts = Post.objects.all()
    profiles = Profile.objects.all()
    return render(request, 'layout/index.html', context={'posts': posts, 'profiles': profiles})


def test(request):
    posts = Post.objects.all()
    return render(request, 'test/test.html')
