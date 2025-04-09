from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:pk>', views.PostView.as_view(), name='post_view'),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("create/", views.CreatePostView.as_view(), name="post_create"),
    path("update/<int:pk>", views.UpdatePostView.as_view(), name="post_update"),
]
