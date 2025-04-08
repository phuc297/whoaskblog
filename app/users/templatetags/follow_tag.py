from django import template

register = template.Library()


def is_following(user_profile, profile):
    if user_profile.following.filter(pk=profile.pk).exists():
        return True
    return False

def is_not_following(user_profile, profile):
    if not user_profile.following.filter(pk=profile.pk).exists():
        return True
    return False

register.filter("is_following", is_following)
register.filter("is_not_following", is_not_following)

