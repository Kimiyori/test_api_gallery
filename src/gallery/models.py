# pylint: disable=protected-access
from __future__ import annotations

from django.conf import settings
from django.db import models


def image_path(instance: ImageModel, filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/gallery/user_<id>/<gallery_name>/original/<filename>
    return (
        f"{instance.gallery._meta.model_name}/"
        f"{instance.gallery.user.id}/"
        f"{instance.gallery.name}/"
        f"original/{filename}"
    )


def image_thumb_path(instance: ImageModel, filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/gallery/user_<id>/<gallery_name>/thumbnail/<filename>
    return (
        f"{instance.gallery._meta.model_name}/"
        f"{instance.gallery.user.id}/"
        f"{instance.gallery.name}/"
        f"thumbnail/{filename}"
    )


class Gallery(models.Model):
    """Gallery table"""

    name = models.CharField(max_length=128)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gallery"
    )

    def __str__(self) -> str:
        return str(self.pk)


class ImageModel(models.Model):
    """Image table"""

    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=image_path, max_length=300, blank=True)
    thumbnail = models.ImageField(
        upload_to=image_thumb_path, max_length=300, blank=True
    )
