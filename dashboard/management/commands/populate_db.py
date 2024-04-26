from random import choice

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from dashboard.management.utils.validator import Validator
from dashboard.management.utils.populator import Populator
from users.models import Family

User = get_user_model()


class Command(BaseCommand):
    """ Парсер служит для запуска генерации популяции БД """

    def add_arguments(self, parser):
        parser.add_argument('admin', type=int, default=0, help='Количество администраторов')
        parser.add_argument('staff', type=int, default=0, help='Количество преподавателей')
        parser.add_argument('parents', type=int, default=0, help='Количество родителей')
        parser.add_argument('students', type=int, default=0, help='Количество студентов')

    def handle(self, *args, **options):
        """ --------------------------------------------
            Сгенерируем популяцию
            --------------------------------------------
        Для корректной генерации расписания необходимо при первой генерации указать не менее 20 преподавателей (staff).
        При запуске без параметров используется количество по умолчанию равное нулю.
        При каждом повторном запуске происходит реконфигурация связей, например, учителей и студентов с отделениями,
        при этом данные учетных записей не меняются.
        """
        admin, staff, parents, students = (
            options.get('admin'), options.get('staff'), options.get('parents'), options.get('students'))
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
        # Научим преподавателей - привяжем к отделениям
        # --------------------------------------------
        Populator.link_teachers_to_courses()
        # --------------------------------------------
        # Привяжем студентов к предметам
        # --------------------------------------------
        Populator.link_students_to_courses()
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
        # Важно!
        # Перед генерацией новостей необходимо в модели Article
        # в полях: time_created и time_updated отключить auto_now
        # после чего можно раскомментировать следующий вызов
        Populator.generate_news()
        # после генерации выполнить инструкции в обратном порядке
        # --------------------------------------------
        print('Готово')
        # --------------------------------------------
