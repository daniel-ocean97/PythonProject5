from django.contrib import admin

from .models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "pk")
    list_filter = ("email",)
    search_fields = ("email",)


@admin.register(Payment)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user", "amount")
    list_filter = ("user",)
    search_fields = ("user",)