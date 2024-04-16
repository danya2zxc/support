from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager

from users.enums import Role


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        user = self.model(
            email=self.normalize_email(email=email), **extra_fields
        )

        setattr(user, "password", make_password(password))
        user.save()

        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields
    ):
        return self.create_user(
            email=email,
            password=password,
            is_superuser=True,
            is_active=True,
            is_staff=True,
            role=Role.ADMIN,
        )
