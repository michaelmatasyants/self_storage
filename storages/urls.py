from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.show_faq, name='faq'),
    path('boxes', views.choose_boxes, name='boxes'),
    path('my_rent/', views.show_personal_account, name='my_rent'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path(
        "logout",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
    path('send_mail/', views.send_payment_link, name='send_mail'),
]
