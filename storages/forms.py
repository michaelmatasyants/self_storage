from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from storages.models import CustomUser


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                   "placeholder": "E-mail"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                   "placeholder": "Пароль"}
        )
    )


class RegistrationForm(UserCreationForm):

    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                   "placeholder": "E-mail"}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                   "placeholder": "Имя", "required": False}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                "placeholder": "Фамилия",
                "required": False,
            }
        )
    )
    phonenumber = PhoneNumberField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                "placeholder": "Телефон",
                "required": False,
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                   "placeholder": "Пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 " "SelfStorage__bg_lightgrey",
                   "placeholder": "Подтверждение пароля"}
        )
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phonenumber",
            "password1",
            "password2",
        )