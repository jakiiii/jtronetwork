from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from apps.accounts.models import User

from apps.accounts.forms import UserAdminCreationForm, UserAdminChangeForm


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User

    list_display = ['username', 'get_full_name', 'email', 'is_superuser', 'is_staff', 'is_active']
    list_filter = ['is_superuser', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Others', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff', 'is_examiner', 'is_examine')}
         ),
    )


admin.site.unregister(Group)
