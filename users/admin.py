from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'role',
        'bio',
    )
    search_fields = (
        'first_name'
        'last_name'
        'username',
        'email',
    )
    list_filter = ('username',)
    empty_value_display = '-пусто-'
