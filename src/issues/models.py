from typing import Any

from django.db import models


class Issue(models.Model):
    junior_id: Any = models.IntegerField()
    senior_id: Any = models.IntegerField()
    title: Any = models.CharField(max_length=100)
    body: Any = models.TextField()
