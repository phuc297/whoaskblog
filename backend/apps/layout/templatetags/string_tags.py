from django import template

register = template.Library()


def cut(string):
    return string[:35]

def shorten(text, word_limit=10):
    words = text.split()
    shortened = " ".join(words[:word_limit])
    return shortened + ("..." if len(words) > word_limit else "")


register.filter("cut", cut)
register.filter("shorten", shorten)
