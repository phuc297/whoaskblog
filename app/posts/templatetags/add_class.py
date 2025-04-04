from django import template

register = template.Library()


def add_class(value, arg):
    return value.as_widget(attrs={"class": arg})


register.filter("add_class", add_class)
