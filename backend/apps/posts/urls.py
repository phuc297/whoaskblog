from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:pk>', views.PostView.as_view(), name='view'),
    path("<int:pk>/comment/", views.comment, name="comment"),
    path("<int:pk>/vote/", views.post_vote, name="vote"),
    path("create/", views.CreatePostView.as_view(), name="create"),
    path("<int:pk>/update/", views.UpdatePostView.as_view(), name="update"),
    path("<int:pk>/delete/", views.DeletePostView.as_view(), name="delete"),
    path("list/", views.PublishedPostListView.as_view(), name="list"),
    path("draft-list/", views.DraftPostListView.as_view(), name="draft"),
    path("<int:pk>/summarize", views.summarize_post, name="summarize"),
    path("create/<int:pk>/tags/", views.CreateTagView.as_view(), name="create_tags"),
]
