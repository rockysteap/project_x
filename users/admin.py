from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from project_x.settings import MEDIA_HOSTING
from users.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (('Пользователь', {'fields': ('show_photo', 'type',)}),) + UserAdmin.fieldsets
    list_display = ('username', 'show_photo', 'email', 'first_name', 'last_name', 'type', 'is_staff')
    search_fields = UserAdmin.search_fields + ('username__startswith', )
    UserAdmin.list_filter += ('type',)
    readonly_fields = UserAdmin.readonly_fields + ('show_photo',)
    save_on_top = True

    @admin.display(description="Фото")
    def show_photo(self, obj):
        if obj.photo:
            url = f'{obj.photo.url}'
            if MEDIA_HOSTING in url:
                url = f'{url.replace('/media', 'https:/')}'
                return mark_safe(f"<img src='{url}' width=50>")
        return 'Без фото'


admin.site.register(User, CustomUserAdmin)
