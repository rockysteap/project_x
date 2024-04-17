from django.contrib.auth import get_user_model
from django.db import models


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
