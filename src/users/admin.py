from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .enums import Role

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "role"]
    exclude = ["user_permissions", "groups"]
    readonly_fields = [
        "password",
        "last_login",
        "date_joined",
        "is_superuser",
        "email",
    ]
    actions = ["set_junior", "set_senior", "set_admin"]

    @admin.action(description="Set selected User to role Junior")
    def set_junior(self, request, qs: QuerySet):
        count_update = qs.update(role=Role.JUNIOR)
        self.message_user(
            request, f"{count_update} User was updated to Junior"
        )

    @admin.action(description="Set selected User to role Senior")
    def set_senior(self, request, qs: QuerySet):
        count_update = qs.update(role=Role.SENIOR)
        self.message_user(
            request, f"{count_update} User was updated to Senior"
        )

    @admin.action(description="Set selected User to role Admin")
    def set_admin(self, request, qs: QuerySet):
        count_update = qs.update(role=Role.ADMIN)
        self.message_user(request, f"{count_update} User was updated to Admin")
