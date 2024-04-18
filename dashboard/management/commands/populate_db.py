from random import choice

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from dashboard.management.utils.validator import Validator
from dashboard.management.utils.populator import Populator
from dashboard.models import Teacher
from users.models import Family

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        # --------------------------------------------
        # Сгенерируем популяцию
        # --------------------------------------------
        # Для корректной генерации расписания необходимо
        # изначально сгенерировать минимум 20 учителей (staff)
        admin, staff, parents, students = 0, 0, 0, 0
        # admin, staff, parents, students = 2, 20, 50, 75
        for _ in range(admin):
            Populator.create_new_user(User.Types.ADMIN)
        for _ in range(staff):
            Populator.create_new_user(User.Types.STAFF)
        for _ in range(parents):
            Populator.create_new_user(User.Types.PARENT)
        for _ in range(students):
            Populator.create_new_user(User.Types.STUDENT)
        # --------------------------------------------
        # Сгенерируем семейные связи (родитель-ребенок(студент))
        # --------------------------------------------
        parents = User.objects.filter(type=User.Types.PARENT).order_by('?')
        students = User.objects.filter(type=User.Types.STUDENT).order_by('?')
        for i in range(len(students)):
            if not Validator.is_value_present_in_db(students[i].pk, Family, 'student_id'):
                Family.objects.create(parent=choice(parents), student=students[i])
        # --------------------------------------------
        # Сгенерируем отделения и предметы в них
        # --------------------------------------------
        Populator.create_courses()
        Populator.create_subjects()
        # --------------------------------------------
        # Научим преподавателей - привяжем к предметам
        # --------------------------------------------
        Teacher.objects.all().delete()
        Populator.link_teachers_to_courses()
        # --------------------------------------------
        # Добавим аудитории
        # --------------------------------------------
        Populator.create_classrooms(1, 9)
        # --------------------------------------------
        # Расписание
        # --------------------------------------------
        # Сгенерируем временнЫе слоты на неделю
        # --------------------------------------------

        Populator.parse_schedule_grid_to_db()
        # --------------------------------------------
        # Сгенерируем расписание на неделю
        # --------------------------------------------
        Populator.generate_schedule()
        # --------------------------------------------
        # Сгенерируем новости
        # --------------------------------------------
        # Populator.generate_news()

        # print(Populator.get_news_with_titles())
        print(Populator.get_images_by_filter('N', 'NEWS'))
        # --------------------------------------------
        #
