from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from .enums import Role
from .models import ActivationKey, User
from .services import Activator


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

        # activation_key: uuid.UUID = services.create_activation_key(
        #     email=serializer.data["email"]
        # )
        # services.send_user_activation_email(
        #     email=serializer.data["email"], activation_key=activation_key
        # )

        activator_service = Activator(email=serializer.data["email"])
        activation_key = activator_service.create_activation_key()
        activator_service.send_user_activation_email(
            activation_key=activation_key
        )

        activator_service.save_activation_information(
            internal_user_id=serializer.instance.id,
            activation_key=activation_key,
        )
        return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["POST"])
@permission_classes([permissions.AllowAny])
def activate_mail(request) -> Response:
    activation_key = request.data.get("activation_key")
    email = request.data.get("email")
    user = User.objects.get(email=email)
    activator_service = Activator(email=email)

    if user.is_active is True:
        return Response(
            {"message": "User is already activated"},
            status=200,
        )

    try:
        activation = ActivationKey.objects.get(key=activation_key)
    except ActivationKey.DoesNotExist:
        return Response(
            {"message": "Activation key does not exist"},
            status=404,
        )

    else:
        activator_service.validate_activation(
            user,
            activation=activation,
        )
        return Response(
            {"message": "Email activated successfully"},
            status=200,
        )


@api_view(http_method_names=["POST"])
@permission_classes([permissions.AllowAny])
def resend_activation_mail(request) -> Response:
    email = request.data.get("email")
    user = User.objects.get(email=email)
    if user.is_active is True:
        return Response(
            {"message": "User is already activated"},
            status=200,
        )

    activator_service = Activator(email=email)
    activation_key = activator_service.create_activation_key()
    activator_service.send_user_activation_email(activation_key=activation_key)
    activator_service.save_activation_information(
        activation_key=activation_key, internal_user_id=user.id
    )
    return Response(
        {"message": "Activation mail resend on your email"},
        status=200,
    )


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
