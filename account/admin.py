from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.forms import AccountCreationForm,AccountChangeForm
from.models import AccountUser

class CustomUserAdmin(UserAdmin):
    add_form = AccountCreationForm
    form = AccountChangeForm
    model = AccountUser
    list_display = ["first_name","last_name"]
    

# Register your models here.
admin.site.register(AccountUser,UserAdmin)
