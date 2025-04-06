from django.db import models

from users.models import Profile


class Conversation(models.Model):
    title = models.TextField(blank=True)
    members = models.ManyToManyField(Profile, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        if not self.title:
            self.title = f"{self.members[0]} and {self.members[1]}"
        return super().save(force_insert, force_update, using, update_fields)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='sent_messages' , on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content}"
    
    
