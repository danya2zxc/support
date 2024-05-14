import uuid
from dataclasses import dataclass

from shared.cache import CacheService

from .enums import ActivationType
from .models import User
from .tasks import send_activation_mail, send_succes_validate_mail


@dataclass
class ActivatiorUserMeta:
    user_id: int


class Activator:

    def __init__(self, email: str | None = None) -> None:
        self.email = email

    def create_activation_key(self):
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)

    def create_activation_link(self, activation_key: uuid.UUID):
        return f"https://frontend.com/users/activate/{activation_key}"

    def send_user_activation_email(self, activation_key: uuid.UUID):

        activation_link = self.create_activation_link(activation_key)

        send_activation_mail.delay(
            recipient=self.email,
            activation_link=activation_link,
        )

    def save_activation_information(
        self,
        internal_user_id: int,
        activation_key: uuid.UUID,
    ):

        cache = CacheService()
        payload = {"user_id": internal_user_id}
        cache.save(
            namespace="activation",
            key=str(activation_key),
            instance=payload,
            ttl=2_000,
        )

    def validate_activation(self, activation_key: str):
        cache = CacheService()

        record = cache.get(namespace="activation", key=activation_key)

        if record is None:
            return ActivationType.KEY_NOT_FOUND_OR_TTL_EXPIRED

        else:
            instance = ActivatiorUserMeta(**record)
            user = User.objects.get(id=instance.user_id)
            user.is_active = True
            user.save()
            self.email = user.email
            cache.delete(namespace="activation", key=str(activation_key))

            send_succes_validate_mail.delay(recipient=user.email)

            return ActivationType.SUCCESS
