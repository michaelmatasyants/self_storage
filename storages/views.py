from django.shortcuts import render, redirect
from django.db.models import Prefetch, Count
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from storages.backends import EmailBackend
from storages.forms import LoginForm
from storages.models import CustomUser, Storage, Box, Order #, FAQ, BoxType


def serialize_storage(storage: Storage):
    return {
        'city': storage.city,
        'address': storage.address,
        # 'temp': str(storage.temp),
        'photo': storage.photo.url
    }


def serialize_user(user: CustomUser):
    return {

    }


# def serialize_faq(question: FAQ):
#     return {
#         'question': question.question,
#         'answer': question.answer,
#     }


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
    return render(request, "index.html", {"form": form})


def index(request):
    nearest_storage = Storage.objects.first()
    context = {
        'nearest_storage': serialize_storage(nearest_storage)
    }
    return render(request, 'index.html', context=context)


# Не хватает BoxType
def choose_boxes(request):
    # storages = Storage.objects.prefetch_related(
    #     Prefetch('boxes', queryset=Box.objects.filter(is_free=True))
    # )
    # serialize_storages = []
    # for storage in storages:
    #     free_boxes = storage.boxes.all()
    #     if not free_boxes:
    #         continue

    #     storage_box_types = free_boxes.values('box_type').distinct()
    #     serialize_storages.append({
    #         'storage': serialize_storage(storage),
    #         'free_boxes_count': free_boxes.count(),
    #         'storage_box_types': storage_box_types
    #     })

    # context = {'storages': serialize_storages}
    # return render(request, 'boxes.html', context=context)
    return render(request, 'boxes.html')


# не дописан
def show_personal_account(request):
    user = request.user
    
    orders = user.orders.all()
    context = {
        'user': serialize_user(user),
        'orders': orders
    }
    return render(request, 'my-rent.html', context=context)


# def show_faq(request):
#     context={
#         'questions': [
#             serialize_faq(question) for question in FAQ.objects.all()
#         ]
#     }
#     return render(request, 'faq.html', context=context)
