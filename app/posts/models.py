from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random

colors = [
    "red",
    "yellow",
    "green",
    "blue",
    "pink",
    "purple"
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    color = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        available_colors = set(
            colors) - set(Category.objects.values_list("color", flat=True))
        if available_colors:
            self.color = random.choice(list(available_colors))
        else:
            raise ValueError("No available colors left to assign.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ManyToManyField("self", symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
