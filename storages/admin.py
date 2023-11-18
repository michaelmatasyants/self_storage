from django.contrib import admin

from storages.models import CustomUser, Storage, Box, Order, BoxType


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone']


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(BoxType)
class BoxTypeAdmin(admin.ModelAdmin):
    pass
