from django.contrib import admin
from django.urls import path
from storages import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('boxes', views.choose_boxes, name='choose_boxes'),
    path('profile/<int:user_id>/', views.show_personal_account, name='profile'),
    # path('faq', views.show_faq, name='choose_boxes'),
]
