from django import template

register = template.Library()


def cut(string):
    return string[:35]


register.filter("cut", cut)
