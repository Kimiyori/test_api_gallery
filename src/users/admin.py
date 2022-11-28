from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from users.forms import UserChangeForm, UserCreationForm
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User admin"""

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "id",
        "username",
        "email",
        "password",
    ]
    list_filter = ("is_superuser",)

    fieldsets = (
        (
            None,
            {"fields": ("email", "is_active", "is_staff", "is_superuser", "password")},
        ),
        ("Personal info", {"fields": ("username",)}),
        ("Groups", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("user_permissions",)}),
    )
    add_fieldsets = (
        (
            None,
            {"fields": ("email", "is_staff", "is_superuser", "password", "password2")},
        ),
        ("Personal info", {"fields": ("username",)}),
        ("Groups", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("user_permissions",)}),
    )

    search_fields = (
        "email",
        "username",
    )
    ordering = ("email",)
    filter_horizontal = ()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user_permissions":
            kwargs["queryset"] = Permission.objects.all().select_related("content_type")
        return super().formfield_for_manytomany(db_field, request, **kwargs)
