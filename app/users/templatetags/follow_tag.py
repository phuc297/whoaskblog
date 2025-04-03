from django import template

register = template.Library()


def check_following(user_profile, profile):
    if user_profile.following.filter(pk=profile.pk).exists():
        return True
    return False


register.filter("check_following", check_following)
