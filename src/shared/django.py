from django.db import models


class TimeStampMixin(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
