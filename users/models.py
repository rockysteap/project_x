from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        M = 'M'
        F = 'F'

    class Types(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        STAFF = 'STAFF', 'staff'
        PARENT = 'PARENT', 'parent'
        STUDENT = 'STUDENT', 'student'

    address = models.CharField(blank=True, null=True, max_length=100, verbose_name='Адрес')
    passport = models.CharField(blank=True, null=True, max_length=100, verbose_name='Данные паспорта')
    type = models.CharField(max_length=7, choices=Types.choices, default=Types.STUDENT, verbose_name='Тип записи')
    gender = models.CharField(blank=True, null=True, max_length=1, choices=Gender.choices)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(validators=[phoneNumberRegex], blank=True, null=True, max_length=16, unique=True,
                                    verbose_name='Номер телефона')
    photo = models.ImageField(upload_to="users/images/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    memo = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Family(models.Model):
    parent = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='students')
    student = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, null=True, blank=True,
                                related_name='parents')

    def __str__(self):
        return f'{self.parent}: {self.student}'
