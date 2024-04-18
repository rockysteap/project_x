from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, RedirectView, View

from dashboard.forms import AddArticleForm
from dashboard.models import Article, Course
from dashboard.utils import ExtraContextMixin


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Похоже страницу украли!</h1>')


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
        return Article.objects.order_by('-time_updated')


class ShowCourses(ExtraContextMixin, ListView):
    template_name = 'dashboard/courses.html'
    context_object_name = 'courses'
    template_title = 'Отделения'

    def get_queryset(self):
        return Course.objects.all()
