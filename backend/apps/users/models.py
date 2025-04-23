import random

from django.contrib.auth.models import User
from django.db import models
from utils.utils import get_random_avatar



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name='following', blank=True)
    avatar = models.ImageField(
        upload_to='avatars', default=get_random_avatar,  blank=True, null=True)

    def __str__(self):
        return self.user.username
