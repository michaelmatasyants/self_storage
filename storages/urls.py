from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('boxes/', views.boxes, name='boxes'),
    path('my_rent/', views.my_rent, name='my_rent'),
    path('login/', views.login_user, name='login'),
]
