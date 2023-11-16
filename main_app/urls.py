from django.contrib import admin
from django.urls import path
from storages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', views.login_user, name='login'),
    # path('registration/', views.register_user, name='registration'),
    # path('logout/', views.logout_user, name='logout'),
]
