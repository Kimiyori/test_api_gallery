from rest_framework.permissions import BasePermission
from django.http import HttpRequest
from django.views.generic.base import View
from gallery.models import Gallery


class IsAuthenticatedAndOwner(BasePermission):
    """Permission,that check that user is auth and can get access only to its own galleries"""

    message = "You must be the owner of this object."

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        return request.user and request.user.is_authenticated  # type: ignore

    def has_object_permission(
        self, request: HttpRequest, view: View, obj: Gallery
    ) -> bool:
        return obj.user.id == request.user.id
