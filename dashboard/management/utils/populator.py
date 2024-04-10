from datetime import timedelta, time
from random import choice, randint

from django.contrib.auth import get_user_model
from django.utils import timezone

from dashboard.management.utils.data_reader import DataReader
from dashboard.management.utils.validator import Validator
from dashboard.management.utils.translit import Transliterate
from dashboard.models import Course, Subject, ScheduleGrid


class DBPopulateHelper:
    data = DataReader()

    @staticmethod
    def get_random_gender():
        return choice(['M', 'F'])

    @staticmethod
    def gen_unique_random_phone_number():
        for _ in range(999):
            phone_number = f"+7{''.join([str(randint(0, 9)) for _ in range(10)])}"
            if not Validator.is_value_present_in_db(phone_number, get_user_model(), 'phone_number'):
                return phone_number

    @staticmethod
    def gen_username(first_name, last_name):
        return f"{Transliterate.transliterate_ru_to_en(first_name)}_{Transliterate.transliterate_ru_to_en(last_name)}"

    @staticmethod
    def gen_email(username):
        return f"{username}@mail.ml"

    @staticmethod
    def gen_birthday(user_type: get_user_model().Types) -> timezone:
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

    def get_unique_random_male_fullname(self) -> tuple[str, str]:
        for _ in range(999):  # максимальное кол-во попыток
            f, l = choice(self.data.men_first_names), choice(self.data.men_last_names)
            if not Validator.is_value_present_in_db(self.gen_username(f, l), get_user_model(), 'username'):
                return f, l

    def get_unique_random_female_fullname(self) -> tuple[str, str]:
        for _ in range(999):  # максимальное кол-во попыток
            f, l = choice(self.data.women_first_names), choice(self.data.women_last_names)
            if not Validator.is_value_present_in_db(self.gen_username(f, l), get_user_model(), 'username'):
                return f, l

    def get_random_full_name(self, gender):
        if gender == 'M':
            return self.get_unique_random_male_fullname()
        if gender == 'F':
            return self.get_unique_random_female_fullname()

    def create_new_user(self, user_type):
        gender = self.get_random_gender()
        first_name, last_name = self.get_random_full_name(gender)
        username = self.gen_username(first_name, last_name)
        print(username)
        get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=username,
            is_active=True,
            is_superuser=False,
            is_staff=True if user_type in [get_user_model().Types.ADMIN, get_user_model().Types.STAFF] else False,
            email=self.gen_email(username),
            phone_number=self.gen_unique_random_phone_number(),
            gender=gender,
            type=user_type,
            date_of_birth=self.gen_birthday(user_type),
        )

    @staticmethod
    def create_new_course(course_title):
        if not Validator.is_value_present_in_db(course_title, Course, 'title'):
            Course.objects.create(title=course_title, description=course_title)

    @staticmethod
    def create_new_subject(subject_title, course_title):
        if not Validator.is_value_present_in_db(subject_title, Subject, 'title'):
            Subject.objects.create(title=subject_title, course=course_title, description=subject_title)

    @staticmethod
    def parse_schedule_grid_to_db(self):
        # print(now().isoweekday())  # 2
        # ScheduleGrid.objects.all().delete()
        for day in range(1, 7):  # (воскресенье выходной)
            for enum, item in enumerate(self.data.schedule_grid, start=1):
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
