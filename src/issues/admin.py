from django.contrib import admin
from django.db.models import QuerySet
from django.utils import timezone

from .enums import Status
from .models import Issue, Message


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    model = Issue
    list_display = ["id", "title", "status", "junior", "senior"]
    extra = 1
    actions = ["set_opened", "set_in_progress", "set_closed"]
    list_display_links = ["id", "title"]
    search_fields = ["title"]

    @admin.action(description="Set selected issue to status Opened")
    def set_opened(self, request, qs: QuerySet):
        count_update = qs.update(status=Status.OPENED)
        self.message_user(
            request, f"{count_update} issue was updated to Opened"
        )

    @admin.action(description="Set selected issue to status In progress")
    def set_in_progress(self, request, qs: QuerySet):
        count_update = qs.update(status=Status.IN_PROGRESS)
        self.message_user(
            request, f"{count_update} issue was updated to In progress"
        )

    @admin.action(description="Set selected issue to status Closed")
    def set_closed(self, request, qs: QuerySet):
        count_update = qs.update(status=Status.CLOSED)
        self.message_user(
            request, f"{count_update} issue was updated to Closed"
        )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ["id", "body", "timestamp", "issue_id", "user_id"]
    readonly_fields = ["issue", "user"]
    extra = 1
    list_display_links = ["id", "body"]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_date = timezone.now()
        obj.save()
