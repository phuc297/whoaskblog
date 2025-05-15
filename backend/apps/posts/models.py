from django.conf import settings
from django.forms import ValidationError
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.db import models
from django.core.files import File
from django.utils.text import slugify
from apps.users.models import Profile
from django.utils.timezone import now
import random
from utils.utils import get_random_thumbnail


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    color = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    author = models.ForeignKey(
        Profile, related_name='posts', on_delete=models.CASCADE)
    title = models.TextField(max_length=150)
    content = QuillField()
    # content = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_published_update_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    votes = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)
    views = models.IntegerField(default=0)
    thumbnail = models.ImageField(
        upload_to='images/thumnail_posts/', default=get_random_thumbnail, null=True, max_length=500)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        if not self.category:
            self.category, _ = Category.objects.get_or_create(name='Uncategorized')

        if not self._state.adding:
            previous = Post.objects.get(pk=self.pk)

            if previous.status == Post.DRAFT and self.status == Post.PUBLISHED:
                if not self.published_at:
                    self.published_at = now()

            elif previous.status == Post.PUBLISHED:
                if not self.published_at:
                    self.published_at = now()
                else:
                    self.last_published_update_at = now()

        else:
            if self.status == Post.PUBLISHED:
                self.published_at = now()

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_user_vote(self, profile_id):
        profile = Profile.objects.get(pk=profile_id)
        vote = self.post_votes.filter(voted_by=profile).first()
        return vote.value if vote else None

    def clean(self):
        if self.status == Post.PUBLISHED and not self.category:
            raise ValidationError('Category cannot be null.')

    class Meta:
        ordering = ['-created_at']


class PostVote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )

    post = models.ForeignKey(Post, related_name='post_votes',
                             on_delete=models.CASCADE)
    voted_by = models.ForeignKey(
        Profile, related_name='votes', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voted_by', 'post')

    def __str__(self):
        return f"{self.voted_by} voted {self.get_value_display()} on {self.post}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    parent = models.ManyToManyField("self", symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
