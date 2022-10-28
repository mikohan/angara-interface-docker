from django import template

register = template.Library()

@register.filter(name='trim')
def trim(value, arg=' '):
    if arg != ' ':
        return value.strip(arg)
    else:
        return value.strip()
    