from django import template

register = template.Library()


@register.simple_tag
def file_name(value):
    value = str(value)
    return value[value.rfind('/') + 1:]
