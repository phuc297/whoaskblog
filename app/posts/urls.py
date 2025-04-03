from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('<int:pk>', views.PostView.as_view(), name='post_view'),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("create/", views.post_create, name="post_create"),
]
