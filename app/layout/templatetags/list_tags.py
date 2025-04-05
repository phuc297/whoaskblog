from django import template

register = template.Library()


def head(set):
    return set[:5]


register.filter("head", head)
