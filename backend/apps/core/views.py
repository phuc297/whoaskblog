from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
from apps.posts.models import Post
from apps.posts.services import get_published_posts
from apps.users.models import Profile
from django.views.generic import DetailView


def index(request):
    tabs = {
        "new": "Bài viết mới",
        "popular": "Phổ biến",
        # "trend": "Xu hướng",
        "most_voting": "Được yêu thích",
        "most_discussed": "Thảo luận nhiều",
    }
    tab = request.GET.get("tab", "new")
    posts = get_published_posts()

    if tab == "popular":
        posts = posts.order_by("-views")
    # elif tab == "trend":
    #     posts = posts.order_by("-views")
    elif tab == "most_voting":
        posts = posts.annotate(num_post_votes=Count(
            'post_votes')).order_by("-num_post_votes")
    elif tab == "most_discussed":
        posts = posts.annotate(num_comments=Count(
            'comments')).order_by("-num_comments")
    else:
        posts = posts.order_by("-created_at")

    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_profiles = Profile.objects.annotate(
        num_posts=Count('posts')).order_by('-num_posts')[:3]

    return render(request, 'index/index.html', context={
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'active_tab': tab,
        'tabs': tabs,
        'top_profiles': top_profiles})


def test(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'test/test.html', context={'page_obj': page_obj, 'posts': page_obj.object_list})
