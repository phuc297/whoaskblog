import json
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, ListView, DeleteView, TemplateView, View
from django.db.models import Sum
from .models import Post, Comment, PostVote, Tag
from django.core.exceptions import PermissionDenied
from .forms import PostForm, TagForm
from utils.utils import get_text_post_content
from utils import genai


class CreateTagView(View):
    template_name = 'posts/tag_create.html'

    def get(self, request, pk):
        allowed_post_id = request.session.get('can_tag_post_id')
        if allowed_post_id != pk:
            return HttpResponseForbidden()
        del request.session['can_tag_post_id']

        post = Post.objects.get(pk=pk)
        content_json_string = post.content.json_string
        text_content = get_text_post_content(content_json_string)
        tags = genai.auto_tag_post(post.title, text_content)
        return render(request, self.template_name, {'pk': pk, 'tags': tags})

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)

        tags = self.request.POST.get('tags', '').lower()
        tag_list = [tag.strip()
                    for tag in tags.split(',') if tag.strip()]
        # if len(tag_list) == 0:
        #     content_json_string = post.content.json_string
        #     text_content = get_text_post_content(content_json_string)
        #     tag_list = genai.auto_tag_post(post.title, text_content)

        for tag in tag_list:
            tag_obj, _ = Tag.objects.get_or_create(name=tag)
            post.tags.add(tag_obj)

        return redirect(reverse_lazy('home'))


class CreatePostView(CreateView):
    model = Post
    template_name = 'posts/create.html'
    form_class = PostForm
    published = False

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.profile
        action = self.request.POST.get('action', '').lower()

        if action == 'published':
            self.published = True
            form.instance.status = Post.PUBLISHED

        return super().form_valid(form)

    def get_success_url(self):
        if self.published:
            self.request.session['can_tag_post_id'] = self.object.id
            return reverse_lazy('posts:create_tags', kwargs={'pk': self.object.id})
        return reverse_lazy('home')


class UpdatePostView(UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/update.html'
    form_class = PostForm
    published = False

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user.profile:
            raise PermissionDenied

        return obj

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.profile
        action = self.request.POST.get('action', '').lower()

        if action == 'published':
            self.published = True
            form.instance.status = Post.PUBLISHED

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

# class CreatePostView(View):
#     template_name = 'posts/create.html'

#     def get(self, request):
#         return render(request, self.template_name, {
#             'form': PostForm()
#         })

#     def post(self, request):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = self.request.user.profile
#             action = self.request.POST.get('action', '').lower()
#             if action == 'published':
#                 post.status = Post.PUBLISHED
#             post = form.save()
#             return JsonResponse({'success': True, 'pk': post.id}, status=200)

#         return JsonResponse({'success': False, 'errors': form.errors}, status=400)


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


class PostView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views = obj.views + 1
        obj.save(update_fields=['views'])
        return obj


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
def summarize_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        content_json_string = post.content.json_string
        text_content = get_text_post_content(content_json_string)
        summary = genai.summarize_post(post.title, text_content)
        # tags = genai.add_tags_post(post.title, text_content)
        return JsonResponse({
            'success': True,
            'content': summary
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=500)


def generate_tag(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        content_json_string = post.content.json_string
        text_content = get_text_post_content(content_json_string)
        tags = genai.auto_tag_post(post.title, text_content)
        return JsonResponse({
            'success': True,
            'content': tags
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=500)


@require_POST
@login_required
def comment(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)

    try:
        data = json.loads(request.body)
        content = data.get('content')
        post_id = pk
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
def post_vote(request, pk):
    try:
        data = json.loads(request.body)
        vote_choice = int(data.get('vote', 0))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON input.'}, status=400)

    profile = request.user.profile
    post = get_object_or_404(Post, pk=pk)

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
