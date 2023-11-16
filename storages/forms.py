from django import forms


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
