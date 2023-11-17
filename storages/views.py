from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from storages.forms import LoginForm, RegistrationForm


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    form.add_error(None, ValidationError("Этот аккаунт отключен"))
            else:
                form.add_error(None, ValidationError("Неверный email или пароль."))
    else:
        form = LoginForm()
    return render(request, "aside/login.html", {"form": form})


def register_user(request, *args, **kwargs):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():

            form.save()
            user = authenticate(
                request,
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password1'),
            )
            user = form.cleaned_data.get('email')
            print(type(user), user)
            login(request, user)
            # destination = kwargs.get("next")
            # if destination:
            #     return redirect(destination)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, 'aside/registration.html', {form: form})


def index(request):
    '''Main_page view'''

    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    return render(request, 'index.html', context)


def faq(request):
    '''FAQ view'''
    return render(request, 'faq.html')


def boxes(request):
    '''Boxes view'''
    return render(request, 'boxes.html')


def my_rent(request):
    '''My rent view'''
    return render(request, 'my-rent.html')
