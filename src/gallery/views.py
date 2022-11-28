# pylint: disable=too-many-ancestors, no-member
from typing import Any
from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.serializers import Serializer

from gallery.models import Gallery, ImageModel
from gallery.serializers import (
    GallerySerializer,
    GalleryNotSafeSerializer,
    GalleryUploadImageSerializer,
)
from gallery.permissions import IsAuthenticatedAndOwner
from users.models import User


class GalleryViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    """
    This view provides a post request to register a user.
    """

    queryset = Gallery.objects.select_related("user").prefetch_related("images")
    http_method_names = ["get", "post", "put", "delete"]

    custom_serializers = {
        "list": GallerySerializer,
        "create": GalleryNotSafeSerializer,
        "retrieve": GallerySerializer,
        "update": GalleryNotSafeSerializer,
        "destroy": GalleryNotSafeSerializer,
        "upload_image": GalleryUploadImageSerializer,
    }

    def get_permissions(self) -> list[BasePermission]:
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method in SAFE_METHODS:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedAndOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Serializer:
        return self.custom_serializers[self.action]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(id=request.user.id)
        gallery = Gallery.objects.create(user=user, name=serializer.data["name"])
        headers = self.get_success_headers(serializer.data)
        response_data = {"id": gallery.id, "user_id": user.id}
        response_data.update(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(  # type: ignore
        detail=True,
        methods=["POST"],
        parser_classes=[
            MultiPartParser,
            FormParser,
        ],
    )
    def upload_image(
        self, request: Request, pk: int  # pylint: disable=invalid-name
    ) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = request.data["image"]
        gallery = get_object_or_404(Gallery, pk=pk)
        image = ImageModel.objects.create(gallery=gallery, image=image_file)
        return Response({"image_id": image.id}, status=status.HTTP_200_OK)
