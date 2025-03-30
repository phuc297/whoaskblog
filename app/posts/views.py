from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import Post, Comment


def post_view(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        comment_content = request.POST.get('comment_content')
        post = Post.objects.get(pk=int(request.POST.get('post_id')))
        user = User.objects.get(pk=int(request.POST.get('user_id')))
        comment = Comment.objects.create(post=post, user=user, content=comment_content)
        comment.save()
    return render(request, 'posts/post.html', {'post': post})
