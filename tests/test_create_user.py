import pytest
from rest_framework import status
from django.test.client import Client
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_creation_success(client: Client):
    payload = {
        "email": "john@email.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "role": "junior",
    }

    response = client.post("/users/", data=payload)

    user = User.objects.get(id=1)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

    assert user.first_name == payload["first_name"]
    assert user.last_name == payload["last_name"]


# import pytest
# from rest_framework import status
# from django.test.client import Client
# from django.contrib.auth import get_user_model


# User = get_user_model()


# @pytest.mark.django_db
# def test_user_creation_success(client: Client):
#     payload = {
#         "email": "john@email.com",
#         "password": "password123",
#         "first_name": "John",
#         "last_name": "Doe",
#     }
#     response = client.post("/users/", data=payload)

#     user: User = User.objects.get(id=1)

#     assert response.status_code == status.HTTP_201_CREATED
#     assert User.objects.count() == 1
#     assert user.first_name == payload["first_name"]
#     assert user.last_name == payload["last_name"]


# def test_user_creation_success():
#     url = "http://localhost:8080/users"

#     payload = {
#         "username": "john",
#         "email": "john@email.com",
#         "password": "password123",
#     }
#     response = requests.post(url, json=payload)

#     assert response.status_code == 201
