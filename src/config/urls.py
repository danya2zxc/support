from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import (
    IssueAPI,
    IssueRetrieveUpdateDeleteAPI,
    issues_close,
    issues_take,
    messages_api_dispatcher,
)
from users.api import UserAPI, UserRetrieveUpdateDeleteAPI

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # users
    path("users/", UserAPI.as_view()),
    path("users/<int:id>", UserRetrieveUpdateDeleteAPI.as_view()),
    # issues
    path("issues/", IssueAPI.as_view()),
    path("issues/<int:id>", IssueRetrieveUpdateDeleteAPI.as_view()),
    path("issues/<int:id>/close", issues_close),
    path("issues/<int:id>/take", issues_take),
    # messages
    path("issues/<int:issue_id>/messages", messages_api_dispatcher),
    # Authentication
    path("auth/token/", token_obtain_pair),
]
