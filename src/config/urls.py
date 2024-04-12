from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import IssueAPI, IssueRetrieveUpdateDeleteAPI
from users.api import UserAPI, UserRetrieveUpdateDeleteAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserAPI.as_view()),
    path("users/<int:id>", UserRetrieveUpdateDeleteAPI.as_view()),
    path("issues/", IssueAPI.as_view()),
    path("issues/<int:id>", IssueRetrieveUpdateDeleteAPI.as_view()),
    # Authentication
    path("auth/token/", token_obtain_pair),
]
