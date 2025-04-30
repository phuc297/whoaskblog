from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
from apps.posts.models import Post
from apps.users.models import Profile
from django.views.generic import DetailView


def index(request):
    posts = Post.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_profiles = Profile.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:3]
    return render(request, 'index/index.html', context={'page_obj': page_obj, 'posts': page_obj.object_list, 'top_profiles': top_profiles})


def test(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'test/test.html', context={'page_obj': page_obj, 'posts': page_obj.object_list})
