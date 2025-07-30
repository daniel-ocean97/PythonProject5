from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "pk")
    list_filter = ("email",)
    search_fields = ("email",)
