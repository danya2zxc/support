from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .enums import Role
from .managers import UserManager

# class User(models.Model):
#     password: Any = models.CharField(max_length=100)


class User(AbstractBaseUser, PermissionsMixin):  # type: ignore
    email: models.CharField = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
    )
    first_name: models.CharField = models.CharField(max_length=5, blank=True)
    last_name: models.CharField = models.CharField(max_length=50, blank=True)

    is_staff: models.BooleanField = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    role: models.CharField = models.CharField(
        max_length=15,
        default=Role.JUNIOR,
        choices=Role.choices(),
    )

    date_joined: models.DateTimeField = models.DateTimeField(
        default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """

        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""

        return self.first_name

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.email

    class Meta:
        ordering = ["id"]


class ActivationKey(models.Model):

    user = models.ForeignKey(
        User,
        related_name="activation_key",
        on_delete=models.CASCADE,
    )
    key = models.UUIDField(editable=False)
