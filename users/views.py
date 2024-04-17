from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from dashboard.utils import ExtraContextMixin
from project_x import settings
from users.forms import RegisterUserForm, LoginUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(ExtraContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    # Extra context:
    template_title = 'Авторизация'
    btn_submit_title = 'Авторизоваться'


class RegisterUser(ExtraContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    # Extra context:
    template_title = 'Регистрация'
    btn_submit_title = 'Отправить'


class ProfileUser(LoginRequiredMixin, ExtraContextMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    # Extra context:
    template_title = 'Профиль пользователя'
    btn_submit_title = 'Обновить'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_user_image=settings.DEFAULT_USER_IMAGE)

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
