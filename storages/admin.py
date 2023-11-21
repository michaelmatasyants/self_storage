from django.contrib import admin

from storages.models import Box, BoxType, CustomUser, Order, Storage


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone']


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'box_type', 'is_free']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(BoxType)
class BoxType(admin.ModelAdmin):
    pass
