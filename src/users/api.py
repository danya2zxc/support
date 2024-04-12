from django.contrib.auth.hashers import make_password
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "password": {
                "required": False,
                "write_only": True,
            },
            "role": {"required": False},
        }

    def validate(self, attrs):
        request = self.context["request"]
        if request.method == "POST":
            if "email" and "password" and "role" not in attrs:
                raise serializers.ValidationError(
                    "Email,Password and Role is required"
                )

        return attrs


class UserAPI(generics.ListCreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        user_data = {
            "id": user.id,
            "email": serializer.validated_data.get("email", ""),
            "first_name": serializer.validated_data.get("first_name", ""),
            "last_name": serializer.validated_data.get("last_name", ""),
            "password": "*******",
            "role": serializer.validated_data.get("role", ""),
        }
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"

    def perform_update(self, serializer):
        if "password" in serializer.validated_data:
            password = serializer.validated_data["password"]
            serializer.validated_data["password"] = make_password(password)
        serializer.save()
