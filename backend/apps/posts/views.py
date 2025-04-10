import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import dateformat
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, FormView, UpdateView

from apps.users.models import Profile

from .models import Post, Comment, PostVote


class CreatePostView(CreateView):
    model = Post
    template_name = "posts/create_post.html"
    success_url = reverse_lazy("home")
    fields = ['title', 'category', 'content', 'thumbnail']

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        post = form.save(commit=False)
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    template_name = "posts/update_post.html"
    success_url = reverse_lazy("home")
    fields = ['title', 'category', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        return super().form_valid(form)


class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"


def post_create(request):
    return render(request, template_name="posts/create.html")


def post_comment(request, post_id):
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


@require_POST
def post_vote(request, post_id):
    try:
        data = json.loads(request.body)
        vote_choice = int(data.get('vote', 0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"success": False, "error": "Invalid JSON input."}, status=400)

    profile = request.user.profile
    post = Post.objects.get(pk=post_id)

    if vote_choice not in [PostVote.UPVOTE, PostVote.DOWNVOTE]:
        return JsonResponse({"success": False, "error": "Invalid vote value."}, status=400)

    vote, created = PostVote.objects.get_or_create(
        post=post,
        voted_by=profile,
        defaults={'value': vote_choice}
    )

    if not created:
        if vote.value != vote_choice:
            vote.value = vote_choice
            vote.save()
            message = "Vote updated"
        else:
            vote.delete()
            message = "Vote removed"
            vote_choice = 0
    else:
        message = "Vote added"
        post.save()

    return JsonResponse({
        "success": True,
        "message": message,
        "votes": post.get_votes(),
        "vote_choice": vote_choice
    })
