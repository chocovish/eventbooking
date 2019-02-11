from django.contrib import admin
from .models import Ticket,Event,Category
# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Category)

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'name']

admin.site.register(User, CustomUserAdmin)