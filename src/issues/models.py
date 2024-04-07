from typing import Any

from django.db import models

from users.models import User


class Issue(models.Model):
    title: Any = models.CharField(max_length=100)
    status: Any = models.PositiveSmallIntegerField()

    junior: Any = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="junior_issues",
    )
    senior: Any = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="senior_issues",
        null=True,
    )

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"


# first_issue: Issue | None = Issue.objects.first()
# instance: Issue = Issue.objects.get(id=1)
# issue: Issue = Issue.objects.get(id=1)
# issue.title
# issue.status
# issue.junior.password
# issue.message_set


class Message(models.Model):
    body: Any = models.TextField()
    timestamp: Any = models.DateTimeField(auto_now_add=True)

    user: Any = models.ForeignKey(User, on_delete=models.CASCADE)
    issue: Any = models.ForeignKey(Issue, on_delete=models.CASCADE)

    # update on any update in the column
    # updated_at = models.DateTimeField(auto_now=True)
