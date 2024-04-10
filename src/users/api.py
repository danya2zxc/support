# from rest_framework.response import Response
import json

from django.http import HttpRequest, JsonResponse

from .models import User


def create_user(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        raise NotImplementedError("Only Post requests")

    data: dict = json.loads(request.body)

    user: User = User.objects.create_user(**data)

    # convert to dict

    results: dict = {
        "id": user.id,  # type: ignore
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_active": user.is_active,
    }

    return JsonResponse(data=results)
