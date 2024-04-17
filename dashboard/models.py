from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from dashboard.management.utils.transliterator import Transliterator


class Article(models.Model):
    class Category(models.TextChoices):
        PUBLIC = 'PUBLIC'
        STAFF = 'STAFF'

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles',
                               null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, unique=True)
    category = models.CharField(choices=Category.choices, default=Category.STAFF, max_length=6,
                                verbose_name='Категория')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_posted = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Статус')
    image_main = models.ImageField(blank=True, null=True, upload_to='articles/images/%Y/%m/%d',)
    image_collage = models.ManyToManyField('Image', blank=True, related_name='articles', verbose_name='Изображения')

    def save(self, *args, **kwargs):
        self.slug = slugify(Transliterator.transliterate_ru_to_en(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['-time_created'])
        ]


class Image(models.Model):
    image = models.ImageField(upload_to="articles/images/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография")
    description = models.CharField(verbose_name='Описание', max_length=250, blank=True, null=True)


class Course(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Отделение')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=100, verbose_name='Предмет')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Teacher(models.Model):
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)


class Classroom(models.Model):
    title = models.CharField(max_length=3, verbose_name='Аудитория')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')


class ScheduleGrid(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    week_day = models.IntegerField(choices=Weekday.choices)
    slot_number = models.IntegerField()
    time_start = models.TimeField()
    time_end = models.TimeField()


class Schedule(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    slot = models.ForeignKey('ScheduleGrid', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject}: {self.teacher}({self.classroom})'
