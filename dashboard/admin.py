from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Article, Course, Student, Teacher
from project_x.settings import MEDIA_HOSTING


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'category', 'content', 'time_created', 'time_updated', 'is_published', 'image_main']
    readonly_fields = ['time_created', 'time_updated', 'image_main']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'article_image', 'time_updated', 'category', 'is_published']
    list_display_links = ['title']
    ordering = ['title']
    list_filter = ['is_published', 'category']
    search_fields = ['title', 'content']
    actions = ['set_published', 'set_unpublished']
    save_on_top = True

    @admin.display(description="Изображение")
    def article_image(self, obj):
        if obj.image_main:
            url = f'{obj.image_main.url}'
            if MEDIA_HOSTING in url:
                url = f'{url.replace('/media', 'https:/')}'
                return mark_safe(f"<img src='{url}' width=50>")
        return 'Без изображения'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f'Изменено {count} записей.')

    @admin.action(description="Снять с публикации выбранные записи")
    def set_unpublished(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']
    list_display_links = ['course', 'student']
    list_filter = ['course']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['course', 'teacher']
    list_display_links = ['course', 'teacher']
    list_filter = ['course']
