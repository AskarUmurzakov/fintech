from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

'''
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass
    
'''

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "balance")
    fields = ("username", "email", "balance", "is_active", "is_staff")


# Register your models here.
