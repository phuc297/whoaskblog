from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import dateformat
from django.views.generic import DetailView

from .models import Post, Comment


class PostView(DetailView):
    model = Post
    template_name = "posts/post.html"


def post_comment(request, post_id):
    print("post_comment")
    if request.method == 'GET':
        content = request.GET.get('comment_content')
        post = get_object_or_404(Post, id=int(request.GET.get('post_id')))
        user = get_object_or_404(User, id=int(request.GET.get('user_id')))
        print(f"content: {content}, post: {post}, user: {user}")
        if content:
            comment = Comment.objects.create(post=post, user=user, content=content)
            comment.save()
            return JsonResponse({
                "success": True,
                "username": user.username,
                "content": comment.content,
                "created_at": comment.created_at,
                "avatar": user.profile.avatar.url if hasattr(user, "profile") else "/static/default-avatar.png"
            })
    else:
        return JsonResponse({"success": False, "error": "Invalid request"})
