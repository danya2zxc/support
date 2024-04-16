from rest_framework import generics, permissions, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.enums import Role

from .enums import Status
from .models import Issue


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
        user_role = self.request.user.role
        if user_role in Role.users_staff():
            return IssueDetailSerializer

        return IssueSerializer

    def get_queryset(self):
        user_role = self.request.user.role
        if user_role == Role.ADMIN:
            return Issue.objects.all()
        elif user_role == Role.SENIOR:
            return Issue.objects.filter(status=Status.OPENED).exclude(
                junior__role=Role.SENIOR
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

        user_role = request.user.role
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
