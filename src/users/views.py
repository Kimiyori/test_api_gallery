from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.serializers import Serializer
from users.models import User
from users.permissions import IsAuthenticatedAndOwner
from users.serializers import UserSerializer, UserRegSerializer


class RegisterViewSet(  # pylint: disable=too-many-ancestors
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    """
    This view provides CRUD for users
    """

    http_method_names = ["get", "post", "put", "delete"]
    queryset = User.objects.all()

    def get_permissions(self) -> list[BasePermission]:
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == "POST":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedAndOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Serializer:
        if self.request.method in ("POST", "PUT"):
            return UserRegSerializer
        return UserSerializer

    @action(detail=False)  # type:ignore
    def me(self, request: Request) -> Response:  # pylint: disable=invalid-name
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
