from typing import Any

from django.db import models


class User(models.Model):
    email: Any = models.CharField(max_length=30)
    first_name: Any = models.CharField(max_length=50)
    last_name: Any = models.CharField(max_length=50)
    password: Any = models.CharField(max_length=100)
    role: Any = models.CharField(max_length=20)
