from datetime import timedelta, time
from random import choice, randint, shuffle

from django.contrib.auth import get_user_model
from django.utils import timezone

from dashboard.management.utils.data_reader import DataReader
from dashboard.management.utils.validator import Validator
from dashboard.management.utils.transliterator import Transliterator
from dashboard.models import Course, Subject, ScheduleGrid, Schedule, Classroom, Teacher


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
            f, l = choice(cls.data.men_first_names), choice(cls.data.men_last_names)
            if not Validator.is_value_present_in_db(cls.gen_username(f, l), get_user_model(), 'username'):
                return f, l

    @classmethod
    def get_unique_random_female_fullname(cls) -> tuple[str, str]:
        for _ in range(999):  # максимальное кол-во попыток
            f, l = choice(cls.data.women_first_names), choice(cls.data.women_last_names)
            if not Validator.is_value_present_in_db(cls.gen_username(f, l), get_user_model(), 'username'):
                return f, l

    @classmethod
    def get_random_full_name(cls, gender):
        if gender == 'M':
            return cls.get_unique_random_male_fullname()
        if gender == 'F':
            return cls.get_unique_random_female_fullname()

    @classmethod
    def create_new_user(cls, user_type):
        gender = cls.get_random_gender()
        first_name, last_name = cls.get_random_full_name(gender)
        username = cls.gen_username(first_name, last_name)
        # TODO: вернуть юзерам пароли pbkdf2_sha256
        # get_user_model().objects.create(
        get_user_model().objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=username,
            is_active=True,
            is_superuser=False,
            is_staff=True if user_type in [get_user_model().Types.ADMIN, get_user_model().Types.STAFF] else False,
            email=cls.gen_email(username),
            phone_number=cls.gen_unique_random_phone_number(),
            gender=gender,
            type=user_type,
            date_of_birth=cls.gen_birthday(user_type),
        )

    @classmethod
    def create_new_course(cls, course_title):
        if not Validator.is_value_present_in_db(course_title, Course, 'title'):
            Course.objects.create(title=course_title, description=course_title)

    @classmethod
    def create_courses(cls):
        for course in cls.data.courses:
            cls.create_new_course(course)

    @classmethod
    def create_new_subject(cls, subject_title, course_title):
        if not Validator.is_two_values_present_in_same_entry([subject_title, course_title], Subject,
                                                             ['title', 'course_id']):
            Subject.objects.create(title=subject_title, course=course_title, description=subject_title)

    @classmethod
    def create_subjects(cls):
        pointer = 0
        for course in Course.objects.all():
            while pointer < len(cls.data.subjects):
                if cls.data.subjects[pointer] == '<--->':
                    break
                cls.create_new_subject(cls.data.subjects[pointer], course)
                pointer += 1
            pointer += 1

    @classmethod
    def link_teacher_to_course(cls, teacher, course):
        # if not Validator.is_value_present_in_db(teacher.pk, Teacher, 'teacher'):
        if not Validator.is_two_values_present_in_same_entry(
                [teacher.pk, course.pk], Teacher, ['teacher', 'course']):
            Teacher.objects.create(teacher=teacher, course=course)

    @classmethod
    def link_teachers_to_courses(cls):
        courses = Course.objects.all()
        teachers = get_user_model().objects.filter(type=get_user_model().Types.STAFF)
        # Распределим преподавателей поровну
        teachers_per_course = len(teachers) / len(courses)
        counter = 0
        for course in courses:
            while counter < len(teachers):
                teacher = teachers[counter]
                cls.link_teacher_to_course(teacher, course)
                counter += 1
                if counter % teachers_per_course == 0:
                    break

    @classmethod
    def create_classrooms(cls, floors, rooms):
        for i in range(1, floors + 1):
            for j in range(1, rooms + 1):
                room = f'{i}.{j}'
                if not Validator.is_value_present_in_db(room, Classroom, 'title'):
                    Classroom.objects.create(title=room, description=f'Аудитория {room}')

    @classmethod
    def parse_schedule_grid_to_db(cls):
        for day in range(1, 7):  # (воскресенье выходной)
            for enum, item in enumerate(cls.data.schedule_grid, start=1):
                # enum - порядковый номер занятия
                #                       остальные 5-12 ежедневно, воскресенье - выходной
                # item - расписание одного урока в формате '10:00-10:45'
                start, end = map(lambda s: s.split(':'), item.split('-'))
                # "start, end" - расписание одного урока в формате "['10', '00'], ['10', '45']"
                time_start = *map(int, start),
                time_end = *map(int, end),
                # утренние занятия только в субботу
                if day != 6 and (time_start[0] < 14 or time_end[0] < 14):
                    continue
                if not (Validator.is_two_values_present_in_same_entry(
                        [day, enum], ScheduleGrid, ['week_day', 'slot_number'])):
                    ScheduleGrid.objects.create(
                        week_day=day,
                        slot_number=enum,
                        time_start=time(*time_start),
                        time_end=time(*time_end),
                    )

    @classmethod
    def get_week_schedule_grid(cls):
        result: dict = {}
        for item in ScheduleGrid.objects.all():
            result.setdefault(item.week_day, [])
            result[item.week_day].append(item.slot_number)
        return result

    @classmethod
    def get_courses_with_subjects(cls):
        result: dict = {}
        for item in Subject.objects.all():
            result.setdefault(item.course_id, [])
            result[item.course_id].append(item.title)
        return result

    @classmethod
    def generate_schedule(cls):
        Schedule.objects.all().delete()
        grid = cls.get_week_schedule_grid()
        subjects_list = cls.get_courses_with_subjects()
        for course, subjects in subjects_list.items():
            # Соберем преподавателей по курсу
            teachers = Teacher.objects.filter(course=course)
            # Определим сдвиг курса пн, ср, пт или вт, чт, сб на основе чет/нечет id
            shift = 1 if course % 2 == 0 else 0  # с какого дня недели начнем 1 или 2
            days_counter, week = 0 + shift, 6
            shuffle(subjects)
            while len(subjects) > 0:
                # Пока есть хотя бы один предмет в учебном курсе,
                if not any(map(lambda x: len(x) > 0, grid.values())):
                    return
                # проходим по дням недели со сдвигом,
                # чтобы сделать плавное распределение по всей неделе
                current_day = days_counter % week + 1  # c % 6 = 0, 1, 2, 3, 4, 5, 0, 1, ..
                if grid.get(current_day, None):
                    teacher = choice(teachers)
                    room = choice(Classroom.objects.all())
                    _slot_id = ScheduleGrid.objects.get(week_day=current_day, slot_number=grid[current_day][0]).pk
                    if not Validator.is_value_present_in_db(_slot_id, Schedule, 'slot_id'):
                        # Проверка на свободный слот в расписании
                        Schedule.objects.create(
                            course=Course.objects.get(pk=course),
                            subject=Subject.objects.get(title=subjects[0], course=course),
                            teacher=teacher,
                            classroom=room,
                            slot=ScheduleGrid.objects.get(week_day=current_day, slot_number=grid[current_day][0]),
                        )
                    grid[current_day].remove(grid[current_day][0])
                    subjects_list[course].remove(subjects[0])
                days_counter += 2

        # print(grid)
        # print(subjects_list)
