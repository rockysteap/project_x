from random import choice

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from dashboard.management.utils.validator import Validator
from dashboard.models import Course, Classroom
from dashboard.management.utils.populator import Populator
from users.models import Family

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Сгенерируем популяцию
        admin, staff, parents, students = 0, 0, 0, 0
        # admin, staff, parents, students = 2, 5, 5, 5
        for _ in range(admin):
            Populator.create_new_user(User.Types.ADMIN)
        for _ in range(staff):
            Populator.create_new_user(User.Types.STAFF)
        for _ in range(parents):
            Populator.create_new_user(User.Types.PARENT)
        for _ in range(students):
            Populator.create_new_user(User.Types.STUDENT)
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
        for course in Populator.data.courses:
            Populator.create_new_course(course)

        pointer = 0
        for course in Course.objects.all():
            while pointer < len(Populator.data.subjects):
                if Populator.data.subjects[pointer] == '<--->':
                    break
                Populator.create_new_subject(Populator.data.subjects[pointer], course)
                pointer += 1
            pointer += 1

        # Добавим аудитории
        for i in range(11, 20):
            Classroom.objects.create(title=i, description=f'Аудитория {i}')
        # --------------------------------------------
        # Расписание
        # Сгенерируем временнЫе слоты на неделю
        Populator.parse_schedule_grid_to_db()

        # print(now().isoweekday())  # 2

        # Сгенерируем расписание
        print(Populator.get_week_schedule_grid())
        print(Populator.get_courses_with_subjects())
        #
        #
        Populator.generate_schedule()
