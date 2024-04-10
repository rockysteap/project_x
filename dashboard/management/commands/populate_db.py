from random import choice

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from dashboard.management.utils.validator import Validator
from dashboard.models import Course, Classroom
from dashboard.management.utils.populator import DBPopulateHelper as Populate
from users.models import Family

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Сгенерируем популяцию
        admin, staff, parents, students = 0, 0, 0, 0
        # admin, staff, parents, students = 2, 5, 10, 10
        for _ in range(admin):
            Populate.create_new_user(User.Types.ADMIN)
        for _ in range(staff):
            Populate.create_new_user(User.Types.STAFF)
        for _ in range(parents):
            Populate.create_new_user(User.Types.PARENT)
        for _ in range(students):
            Populate.create_new_user(User.Types.STUDENT)
        # --------------------------------------------
        """                 memo:
            k = choice(kids)
            print(k.username)
            print(len(kids))
            kids = kids.all().exclude(pk=k.pk)
            print(len(kids))
        """
        # Сгенерируем семейные связи (родитель-ребенок(студент))
        # --------------------------------------------
        # Parent.objects.all().delete()
        # Раскомментировать выше для очистки таблицы Parent и создания новых связей
        parents = User.objects.filter(type=User.Types.PARENT).order_by('?')
        students = User.objects.filter(type=User.Types.STUDENT).order_by('?')
        for i in range(len(students)):
            if not Validator.is_value_present_in_db(students[i].pk, Family, 'student_id'):
                Family.objects.create(parent=choice(parents), student=students[i])
        # --------------------------------------------
        """                  memo:
            for p in parents:
                print(p.students.all())
        """
        # Сгенерируем отделения и предметы в них
        # --------------------------------------------
        for course in Populate.data.courses:
            Populate.create_new_course(course)

        pointer = 0
        for course in Course.objects.all():
            while pointer < len(Populate.data.subjects):
                if Populate.data.subjects[pointer] == '<--->':
                    break
                Populate.create_new_subject(Populate.data.subjects[pointer], course)
                pointer += 1
            pointer += 1

        # Добавим аудитории
        for i in range(11, 20):
            Classroom.objects.create(title=i, description=f'Аудитория {i}')
        # --------------------------------------------
        # Расписание
        Populate.parse_schedule_grid_to_db(Populate)
