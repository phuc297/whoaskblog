from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.users.models import Profile
from utils import utils

from .models import Notification
from apps.posts.models import Comment, Post
from django.contrib.contenttypes.models import ContentType


@receiver(m2m_changed, sender=Profile.followers.through)
def notify_on_new_follower(sender, instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            new_follower = Profile.objects.get(pk=pk)
            Notification.objects.create(
                recipient=instance,
                message=f"{new_follower} has started following you",
                content_type=ContentType.objects.get_for_model(new_follower),
                object_id=pk
            )


@receiver(post_save, sender=Post)
def notify_followers_on_new_post(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        followers = author.followers.all()
        for follower in followers:
            Notification.objects.create(recipient=follower,
                                        message=f"{author} just posted an article",
                                        content_type=ContentType.objects.get_for_model(instance),
                                        object_id=instance.id)


@receiver(post_save, sender=Comment)
def notify_author_on_new_comment(sender, instance, created, **kwargs):
    if created:
        commenter = instance.commenter
        author = instance.post.author

        content = instance.content
        content = utils.short_text(content)
        Notification.objects.create(recipient=author,
                                    message=f"{commenter} commented on your post",
                                    content_type=ContentType.objects.get_for_model(instance),
                                    object_id=instance.id)
