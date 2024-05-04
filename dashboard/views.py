from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, RedirectView, View

from dashboard.forms import AddArticleForm
from dashboard.models import Article, Course, Teacher, Schedule, Student
from dashboard.utils import ExtraContextMixin, week
from project_x import settings


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)


class AboutView(ExtraContextMixin, View):
    template_name = 'dashboard/about.html'
    context_object_name = 'about'
    template_title = 'О нас'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'template_title': self.template_title})


class RedirectToNews(RedirectView):
    permanent = False
    pattern_name = 'news'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)


class AddArticle(PermissionRequiredMixin, LoginRequiredMixin, ExtraContextMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'dashboard/add_article.html'
    template_title = 'Добавить новую статью'
    btn_submit_title = 'Добавить'
    permission_required = 'dashboard.add_article'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        return super().form_valid(form)


class ShowArticle(ExtraContextMixin, DetailView):
    model = Article
    template_name = 'dashboard/article.html'
    context_object_name = 'article'
    slug_url_kwarg = 'article_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, template_title=context['article'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Article.objects.filter(is_published=1), slug=self.kwargs[self.slug_url_kwarg])


class ShowNews(ExtraContextMixin, ListView):
    template_name = 'dashboard/news.html'
    context_object_name = 'news'
    template_title = 'Новости'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-time_updated')


class ShowCourses(ExtraContextMixin, ListView):
    template_name = 'dashboard/courses.html'
    context_object_name = 'courses'
    template_title = 'Отделения'

    def get_queryset(self):
        return Course.objects.all()


class ShowCourseTeachers(ExtraContextMixin, ListView):
    template_name = 'dashboard/teachers.html'
    context_object_name = 'course_teachers'
    template_title = 'Преподаватели'
    slug_url_kwarg = 'course_slug'

    def get_queryset(self):
        return Teacher.objects.filter(course_id=get_object_or_404(Course, slug=self.kwargs['course_slug']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, courses=Course.objects.all())


class ScheduleDataSet:
    @classmethod
    def create_schedule_data_set(cls, user_obj=None, invert_main_key=False):
        """Создадим набор данных из schedule queryset с упрощенными ключами
           Упрощенный ключ - строка в формате '<номер_слота_расписания><порядковый_номер_дня_недели>'
           invert_main_key - строка в формате '<порядковый_номер_дня_недели><номер_слота_расписания>'
           Набор данных в формате: {'Ключ': {'': ''}, {'': ''}, {'': ''},}
        """
        data = {}
        queryset = Schedule.objects.filter(course_id=user_obj.course_id) if user_obj else Schedule.objects.all()
        for schedule in queryset:
            key = (f'{schedule.slot.slot_number}{schedule.slot.week_day}' if not invert_main_key
                   else f'{schedule.slot.week_day}{schedule.slot.slot_number}')
            data.setdefault(key, {})
            data[key]['time_start'] = f'{schedule.slot.time_start}'
            data[key]['time_end'] = f'{schedule.slot.time_end}'
            data[key]['subject'] = f'{schedule.subject.title}'
            data[key]['classroom'] = f'{schedule.classroom.title}'
            data[key]['teacher'] = f'{schedule.teacher.teacher}'
            data[key]['course'] = f'{schedule.course.title}'
        return data


class GenericSchedule(ExtraContextMixin, ListView):
    template_name = 'dashboard/schedule.html'
    context_object_name = 'schedules'
    template_title = 'Общее расписание'

    def get_queryset(self):
        return ScheduleDataSet.create_schedule_data_set()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, courses=Course.objects.all(), week=week,
                                      today=timezone.now().isoweekday())


class StudentSchedule(LoginRequiredMixin, ExtraContextMixin, ListView):
    template_name = 'dashboard/student.html'
    context_object_name = 'student_schedules'
    template_title = 'Кабинет студента'

    def get_queryset(self):
        student = None
        try:
            if self.request.user.is_authenticated:
                student = Student.objects.get(student_id=self.request.user)
        except Student.DoesNotExist:
            return Student.objects.none()
        return ScheduleDataSet.create_schedule_data_set(user_obj=student, invert_main_key=True)

    def get_course(self):
        student = None
        try:
            if self.request.user.is_authenticated:
                student = Student.objects.get(student_id=self.request.user)
        except Student.DoesNotExist:
            return Student.objects.none()
        return student.course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, courses=Course.objects.all(), week=week,
                                      today=timezone.now().isoweekday(),
                                      course=self.get_course(),
                                      default_user_image=settings.DEFAULT_USER_IMAGE)
