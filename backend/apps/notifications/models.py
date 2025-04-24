from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.posts.models import Post
from apps.users.models import Profile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    content_object = models.CharField(max_length=255, blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Notification to {self.recipient}: {self.message}"

    def get_image_object(self):
        related = self.related_object
        if related is None:
            return None
        if hasattr(related, 'avatar'):
            return related.avatar.url if related.avatar else None
        if hasattr(related, 'thumbnail'):
            return related.thumbnail.url if related.thumbnail else None
        if hasattr(related, 'commenter'):
            return related.commenter.avatar.url if related.commenter.avatar.url else None
        return None
