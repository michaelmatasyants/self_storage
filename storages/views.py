from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count, Prefetch
from django.shortcuts import redirect, render

from storages.backends import EmailBackend
from storages.forms import LoginForm, RegistrationForm
from storages.models import FAQ, Box, BoxType, CustomUser, Order, Storage


def serialize_storage(storage: Storage):
    return {
        'city': storage.city,
        'address': storage.address,
        'temp': str(storage.temp),
        'photo': storage.photo.url,
    }


def serialize_user(user: CustomUser):
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
    }


def serialize_faq(question: FAQ):
    return {
        'question': question.question,
        'answer': question.answer,
    }


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
    return render(request, "reg_log_forms/login.html", {"form": form})


def register_user(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'),
            )
            if user:
                login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, 'reg_log_forms/register.html', {'form': form})


def index(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
    }
    nearest_storage = Storage.objects.first()
    context['nearest_storage'] = (serialize_storage(nearest_storage)
                                 if nearest_storage else None)
    return render(request, 'index.html', context=context)


def choose_boxes(request):
    storages = Storage.objects.prefetch_related(
        Prefetch('boxes', queryset=Box.objects.filter(is_free=True))
    )
    serialize_storages = []
    for storage in storages:
        free_boxes = storage.boxes.all()
        if not free_boxes:
            continue

        storage_box_types = free_boxes.values('box_type').distinct()
        serialize_storages.append({
            'storage': serialize_storage(storage),
            'free_boxes_count': free_boxes.count(),
            'storage_box_types': storage_box_types,
        })

    context = {
        'storages': serialize_storages,
        'login_form': LoginForm(),
        'registration_form': RegistrationForm()
    }
    return render(request, 'boxes.html', context=context)


# не дописан
@login_required(login_url="login")
def show_personal_account(request):
    user = request.user

    orders = user.orders.all()
    serialized_orders = []
    for order in orders:
        serialized_orders.append({
            'order': order,
            'box_id': order.box.id,
            'storage_id': order.box.storage.id,
            'storage_address': order.box.storage.address,
            'paid_for_period': f'{order.paid_from} - {order.paid_till}',
            # Добавить оповещать за неделю до
            'time_to_pay': True if order.paid_till else False,
        })
    context = {
        'user': serialize_user(user),
        'orders': serialized_orders,
    }
    return render(request, 'my-rent.html', context=context)


def show_faq(request):
    context = {
        'questions': [
            serialize_faq(question) for question in FAQ.objects.all()
        ]
    }
    return render(request, 'faq.html', context=context)
