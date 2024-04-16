from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .enums import Role
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "password": {
                "required": False,
                "write_only": True,
            },
            "role": {"required": False},
        }

    def validate_role(self, value):
        if value not in Role.users():
            raise ValidationError(
                f"Selected Role must be in {Role.users_values()}"
            )
        return value

    def validate(self, attrs):
        request = self.context["request"]
        attrs["password"] = make_password(attrs["password"])
        if request.method == "POST":
            if "email" and "password" and "role" not in attrs:
                raise serializers.ValidationError(
                    "Email,Password and Role is required"
                )
        return attrs


class UserAPI(generics.ListCreateAPIView):
    http_method_names = ["post", "get"]
    serializer_class = UserSerializer

    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def post(self, request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_data = {
            "email": serializer.validated_data.get("email", ""),
            "first_name": serializer.validated_data.get("first_name", ""),
            "last_name": serializer.validated_data.get("last_name", ""),
            "password": "*******",
            "role": serializer.validated_data.get("role", ""),
        }
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["put", "delete", "get"]
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"

    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        admin = request.user.is_staff
        if not admin:
            raise PermissionDenied(
                f"This method is only available for role {Role.ADMIN}"
            )
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)
