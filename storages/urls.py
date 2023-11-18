from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('boxes/', views.boxes, name='boxes'),
    path('my_rent/', views.my_rent, name='my_rent'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path(
        "logout",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
]
