from django import template

register = template.Library()


@register.filter
def concat_strings(str1, str2):
    return f'{str1 + str2}'


@register.filter
def custom_range(value, start_index=0):
    end_index = value + 1 if start_index == 0 else value + start_index
    return range(start_index, end_index)


@register.filter
def get_item_by_key(dictionary, key):
    # print(dictionary.get(key))  # TODO
    return dictionary.get(key)


@register.simple_tag
def external_image_hosting():
    return 'iimg.su'
