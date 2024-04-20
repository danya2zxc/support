from django.db.models import Q
from rest_framework import generics, permissions, response, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from users.enums import Role

from .enums import Status
from .models import Issue, Message


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        # fields = ["id","title", "body","junior_id"]
        # exlude = ["id"]
        fields = "__all__"

    def validate(self, attrs):

        attrs["status"] = Status.OPENED

        return attrs


class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class IssueAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            user_role = self.request.user.role
        if user_role in Role.users_staff():
            return IssueDetailSerializer

        return IssueSerializer

    def get_queryset(self):

        user_role = self.request.user.role

        if user_role == Role.ADMIN:
            return Issue.objects.all()
        elif user_role == Role.SENIOR:
            return Issue.objects.filter(
                Q(senior=user_role)
                | (Q(senior=None) & Q(status=Status.OPENED))
            )
        elif user_role == Role.JUNIOR:
            return Issue.objects.filter(junior=self.request.user)
        else:
            return Issue.objects.none()

    def post(self, request):
        if request.user.role == Role.SENIOR:
            raise Exception("The role is Senior")
        return super().post(request)


class IssueRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    queryset = Issue.objects.all()
    lookup_url_kwarg = "id"
    permission_classes = [permissions.AllowAny]
    serializer_class = IssueSerializer

    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        user_role = self.request.user.role
        if user_role not in Role.users_staff():
            raise PermissionDenied(
                f"This method is only available for"
                f" role {Role.staff_values()}"
            )

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        admin = request.user.is_staff
        if not admin:
            raise PermissionDenied(
                f"This method is only available for role {Role.ADMIN}"
            )
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = "__all__"

    def save(self):
        if (user := self.validated_data.pop("user", None)) is not None:
            self.validated_data["user_id"] = user.id

        if (issue := self.validated_data.pop("issue", None)) is not None:
            self.validated_data["issue_id"] = issue.id

        return super().save()


class SeniorUserPermission(BasePermission):
    message = "Only senior users can perform this action."

    def has_permission(self, request: Request, view) -> bool:
        return request.user.role == Role.SENIOR


@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id: int):
    if request.method == "GET":
        messages = Message.objects.filter(
            Q(
                issue__id=issue_id,
            )
            & (
                Q(
                    issue__senior=request.user,
                )
                | Q(
                    issue__junior=request.user,
                )
            )
        ).order_by("-timestamp")
        serializer = MessageSerializer(messages, many=True)

        return response.Response(serializer.data)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}
        serializer = MessageSerializer(
            data=payload, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(serializer.validated_data)


@api_view(["PUT"])
@permission_classes([SeniorUserPermission])
def issues_close(request: Request, id: int):
    issue = Issue.objects.get(id=id)

    if (issue.status != Status.IN_PROGRESS) or (issue.senior is None):
        return response.Response(
            {"message": "Issue is not In Progress or senior not set"},
            status=422,
        )
    else:
        issue.status = Status.CLOSED
        issue.save()

    serializers = IssueSerializer(issue)
    return response.Response(serializers.data)


@api_view(["PUT"])
@permission_classes([SeniorUserPermission])
def issues_take(request: Request, id: int):
    issue = Issue.objects.get(id=id)

    if (issue.status != Status.OPENED) or (issue.senior is not None):
        return response.Response(
            {"message": "Issue is not Opened or is senior is set"}, status=422
        )

    else:
        issue.senior = request.user
        issue.status = Status.IN_PROGRESS
        issue.save()

    serializer = IssueSerializer(issue)
    return response.Response(serializer.data)
