# pylint: disable=protected-access
from io import BytesIO
from PIL import Image as PILImage

from django.conf import settings
from django.core.files.base import ContentFile

from gallery.models import Gallery, ImageModel


def create_thumbnail(instance: ImageModel) -> None:
    thumb_size = (400, 400)
    pil_image = PILImage.open(instance.image)
    pil_image = pil_image.convert("RGB")
    pil_image.thumbnail(thumb_size, PILImage.ANTIALIAS)
    temp_thumb = BytesIO()
    pil_image.save(temp_thumb, "JPEG")
    temp_thumb.seek(0)
    instance.thumbnail.save(
        instance.image.name,
        ContentFile(temp_thumb.read()),
        save=False,
    )
    temp_thumb.close()


def generate_gallery_path(instance: Gallery) -> str:
    path = (
        f"{settings.MEDIA_ROOT}"
        f"{instance._meta.model_name}/"
        f"{instance.user.id}/"
        f"{instance.name}"
    )
    return path
