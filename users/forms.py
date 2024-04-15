from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    email = forms.CharField(label='E-mail', widget=forms.EmailInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        required = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким e-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    photo = forms.ImageField(required=False, label='Фото')
    username = forms.CharField(disabled=True, label='Логин')
    email = forms.CharField(disabled=True, label='E-mail')
    date_of_birth = forms.DateField(required=False, label='Дата рождения')
    first_name = forms.CharField(required=False, label="Имя")
    last_name = forms.CharField(required=False, label="Фамилия")

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'address', 'memo']
        widgets = {
            'photo': forms.ImageField(),
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'date_of_birth': forms.DateInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'memo': forms.Textarea(attrs={'cols': 20, 'rows': 5}),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth is not None:
            oldest = date.today().year - 100
            youngest = date.today().year - 5
            if not oldest <= date_of_birth.year <= youngest:
                raise forms.ValidationError(f'Выберите дату между годами {oldest} и {youngest}!')
        return date_of_birth


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput())
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput())
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput())
