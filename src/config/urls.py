from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import create_new_issue, create_random_issue, get_issues
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
    path("issues/", get_issues),
    path("issues/create-random", create_random_issue),
    path("issues/create", create_new_issue),
    # Authentication
    path("auth/token/", token_obtain_pair),
]
