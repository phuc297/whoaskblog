from django.contrib import admin

from .models import Category, Post, Comment, PostVote, Tag

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostVote)