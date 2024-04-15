from django import template
from django.contrib.auth import get_user_model

register = template.Library()


# @register.simple_tag
# def get_user_image():
#     image = get_user_model().image.value
#     print(image)
#     return image
