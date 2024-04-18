from django import template

register = template.Library()


@register.filter
def concat_strings(str1, str2):
    return str1 + str2


@register.simple_tag
def external_image_hosting():
    return 'iimg.su'
