from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from apps.users.models import Profile
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_profile_on_new_user(sender, instance, created, **kwargs):
    if getattr(instance, '_disable_signals', False):
        return
    if created:
        profile = Profile.objects.create(user=instance)
        profile.display_name = instance.username
        profile.save()
