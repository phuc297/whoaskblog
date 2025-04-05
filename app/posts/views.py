from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import dateformat
from django.views.generic import DetailView, CreateView, FormView, UpdateView

from users.models import Profile

from .models import Post, Comment


class CreatePostView(CreateView):
    model = Post
    template_name = "posts/create_post.html"
    success_url = reverse_lazy("home")
    fields = ['title', 'category', 'content']

    def form_valid(self, form):
        print('form is valid')
        form.instance.author = self.request.user
        post = form.save(commit=False)
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    template_name = "posts/update_post.html"
    success_url = reverse_lazy("home")
    fields = ['title', 'category', 'content']

    def form_valid(self, form):
        print('form is valid')
        form.instance.author = self.request.user
        post = form.save(commit=False)
        return super().form_valid(form)


class PostView(DetailView):
    model = Post
    template_name = "posts/post.html"


def post_create(request):
    return render(request, template_name="posts/create.html")


def post_comment(request, post_id):
    print("post_comment")
    if request.method == 'GET':
        content = request.GET.get('comment_content')
        post = get_object_or_404(Post, id=int(request.GET.get('post_id')))
        profile = get_object_or_404(Profile, id=int(request.GET.get('profile_id')))
        if content:
            comment = Comment.objects.create(
                post=post, author=profile, content=content)
            comment.save()
            return JsonResponse({
                "success": True,
                "username": profile.user.username,
                "content": comment.content,
                "created_at": comment.created_at,
                "avatar": profile.avatar.url
            })
    else:
        return JsonResponse({"success": False, "error": "Invalid request"})
