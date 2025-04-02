from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    related_object = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Notification to {self.recipient.username}: {self.title}"
