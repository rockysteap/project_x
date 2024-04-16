from django import template

register = template.Library()


@register.filter
def concat_strings(str1, str2):
    return str1 + str2


@register.simple_tag
def path_filter():
    filter_url = '/media/playground.com'
    return filter_url
