from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('faq/', views.show_faq, name='faq'),
    path('boxes', views.choose_boxes, name='boxes'),
    path('my_rent/<int:user_id>/',
         views.show_personal_account,
         name='my_rent'),
    path('login/', views.login_user, name='login'),
]
