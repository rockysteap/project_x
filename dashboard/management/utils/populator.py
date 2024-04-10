from datetime import timedelta, time
from random import choice, randint

from django.contrib.auth import get_user_model
from django.utils import timezone

from dashboard.management.utils.data_reader import DataReader
from dashboard.management.utils.validator import Validator
from dashboard.management.utils.transliterator import Transliterator
from dashboard.models import Course, Subject, ScheduleGrid


class Populator:
    data = DataReader()

    @classmethod
    def get_random_gender(cls):
        return choice(['M', 'F'])

    @classmethod
    def gen_unique_random_phone_number(cls):
        for _ in range(999):
            phone_number = f"+7{''.join([str(randint(0, 9)) for _ in range(10)])}"
            if not Validator.is_value_present_in_db(phone_number, get_user_model(), 'phone_number'):
                return phone_number

    @classmethod
    def gen_username(cls, first_name, last_name):
        return f"{Transliterator.transliterate_ru_to_en(first_name)}_{Transliterator.transliterate_ru_to_en(last_name)}"

    @classmethod
    def gen_email(cls, username):
        return f"{username}@mail.ml"

    @classmethod
    def gen_birthday(cls, user_type: get_user_model().Types) -> timezone:
        # Для снижения проверок при привязке родителей к детям примем следующий разброс возрастов:
        # админы и преподаватели -> 23 - 65
        # дети (студенты) -> 7 - 15
        # родители -> 33 - 60
        now = timezone.now()
        if user_type in [get_user_model().Types.ADMIN, get_user_model().Types.STAFF]:
            return now - timedelta(days=(365 * randint(23, 65) + randint(1, 365)))
        if user_type == get_user_model().Types.STUDENT:
            return now - timedelta(days=(365 * randint(7, 15) + randint(1, 365)))
        if user_type == get_user_model().Types.PARENT:
            return now - timedelta(days=(365 * randint(33, 60) + randint(1, 365)))

    @classmethod
    def get_unique_random_male_fullname(cls) -> tuple[str, str]:
        for _ in range(999):  # максимальное кол-во попыток
            f, l = choice(Populator.data.men_first_names), choice(Populator.data.men_last_names)
            if not Validator.is_value_present_in_db(Populator.gen_username(f, l), get_user_model(), 'username'):
                return f, l

    @classmethod
    def get_unique_random_female_fullname(cls) -> tuple[str, str]:
        for _ in range(999):  # максимальное кол-во попыток
            f, l = choice(Populator.data.women_first_names), choice(Populator.data.women_last_names)
            if not Validator.is_value_present_in_db(Populator.gen_username(f, l), get_user_model(), 'username'):
                return f, l

    @classmethod
    def get_random_full_name(cls, gender):
        if gender == 'M':
            return Populator.get_unique_random_male_fullname()
        if gender == 'F':
            return Populator.get_unique_random_female_fullname()

    @classmethod
    def create_new_user(cls, user_type):
        gender = Populator.get_random_gender()
        first_name, last_name = Populator.get_random_full_name(gender)
        username = Populator.gen_username(first_name, last_name)
        get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=username,
            is_active=True,
            is_superuser=False,
            is_staff=True if user_type in [get_user_model().Types.ADMIN, get_user_model().Types.STAFF] else False,
            email=Populator.gen_email(username),
            phone_number=Populator.gen_unique_random_phone_number(),
            gender=gender,
            type=user_type,
            date_of_birth=Populator.gen_birthday(user_type),
        )

    @classmethod
    def create_new_course(cls, course_title):
        if not Validator.is_value_present_in_db(course_title, Course, 'title'):
            Course.objects.create(title=course_title, description=course_title)

    @classmethod
    def create_new_subject(cls, subject_title, course_title):
        if not Validator.is_value_present_in_db(subject_title, Subject, 'title'):
            Subject.objects.create(title=subject_title, course=course_title, description=subject_title)

    @classmethod
    def parse_schedule_grid_to_db(cls):
        for day in range(1, 7):  # (воскресенье выходной)
            for enum, item in enumerate(Populator.data.schedule_grid, start=1):
                # enum - порядковый номер занятия
                #                       остальные 5-12 ежедневно, воскресенье - выходной
                # item - расписание одного урока в формате '10:00-10:45'
                start, end = map(lambda s: s.split(':'), item.split('-'))
                # "start, end" - расписание одного урока в формате "['10', '00'], ['10', '45']"
                time_start = *map(int, start),
                time_end = *map(int, end),
                if day != 6 and (time_start[0] < 14 or time_end[0] < 14):
                    continue
                if not (Validator.is_two_values_present_in_same_entry(
                        [day, enum], ScheduleGrid, ['week_day', 'slot_number'])):
                    # утренние занятия только в субботу
                    print(day, enum, time_start, time_end)
                    ScheduleGrid.objects.create(
                        week_day=day,
                        slot_number=enum,
                        time_start=time(*time_start),
                        time_end=time(*time_end),
                    )
