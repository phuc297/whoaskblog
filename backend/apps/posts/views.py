import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView
from django.db.models import Sum
from .models import Post, Comment, PostVote
from django.core.exceptions import PermissionDenied
from .forms import PostForm


class DeletePostView(DeleteView):
    model = Post
    template_name = 'posts/delete.html'

    def get_success_url(self):
        if self.object.status == Post.DRAFT:
            return reverse_lazy('posts:draft')
        return reverse_lazy('posts:list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user.profile:
            raise PermissionDenied

        return obj


class CreatePostView(CreateView):
    model = Post
    template_name = 'posts/create.html'
    success_url = reverse_lazy('home')
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile

        action = self.request.POST.get('action', '').lower()

        if action == 'published':
            form.instance.status = Post.PUBLISHED

        return super().form_valid(form)


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views = obj.views + 1
        obj.save(update_fields=['views'])
        return obj


class UpdatePostView(UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/update.html'
    success_url = reverse_lazy('home')
    form_class = PostForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user.profile:
            raise PermissionDenied

        return obj

    def form_valid(self, form):
        form.instance.author = self.request.user.profile

        action = self.request.POST.get('action', '').lower()

        if action == 'published':
            form.instance.status = Post.PUBLISHED

        return super().form_valid(form)


class PublishedPostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(author=self.request.user.profile, status=Post.PUBLISHED).order_by('-created_at')


class DraftPostListView(ListView):
    model = Post
    template_name = 'posts/draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(author=self.request.user.profile, status=Post.DRAFT).order_by('-created_at')


@require_POST
@login_required
def comment(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    try:
        data = json.loads(request.body)
        content = data.get('content')
        post_id = data.get('post_id')
        profile = request.user.profile
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON input'}, status=400)

    if not content:
        return JsonResponse({'success': False, 'error': 'Empty Comment'}, status=400)

    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        post=post, commenter=profile, content=content)
    comment.save()
    return JsonResponse({
        'success': True,
        'username': profile.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p').lstrip('0').lower(),
        'avatar': profile.avatar.url
    })


@require_POST
@login_required
def post_vote(request, post_id):
    try:
        data = json.loads(request.body)
        vote_choice = int(data.get('vote', 0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON input.'}, status=400)

    profile = request.user.profile
    post = get_object_or_404(Post, pk=post_id)

    if vote_choice not in [PostVote.UPVOTE, PostVote.DOWNVOTE]:
        return JsonResponse({'success': False, 'error': 'Invalid vote value.'}, status=400)

    vote, created = PostVote.objects.get_or_create(
        post=post,
        voted_by=profile,
        defaults={'value': vote_choice}
    )

    if created:
        message = 'Vote added'
    else:
        if vote.value == vote_choice:
            vote.delete()
            message = 'Vote removed'
            vote_choice = 0
        else:
            vote.value = vote_choice
            vote.save()
            message = 'Vote updated'
    total_value = post.post_votes.aggregate(total=Sum('value'))['total'] or 0

    return JsonResponse({
        'success': True,
        'message': message,
        'votes': total_value,
        'vote_choice': vote_choice
    })
