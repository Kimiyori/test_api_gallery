# pylint: disable=unused-argument,no-member
import os
from typing import Any
import shutil

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from gallery.services.image_services import create_thumbnail, generate_gallery_path
from gallery.models import Gallery, ImageModel


@receiver(post_delete, sender=Gallery)
def delete_directory(sender: Any, instance: Gallery, **kwargs: Any) -> None:
    path = generate_gallery_path(instance)
    try:
        shutil.rmtree(path)
    except OSError as error:
        print(f"Error: {error.filename}) - {error.strerror}.")


@receiver(post_delete, sender=ImageModel)
def delete_image(sender: Any, instance: ImageModel, **kwargs: Any) -> None:
    for image in (instance.image.path, instance.thumbnail.path):
        if os.path.isfile(image):
            os.remove(image)


@receiver(pre_save, sender=ImageModel)
def save_image_files(sender: Any, instance: ImageModel, **kwargs: Any) -> None:
    try:
        this = ImageModel.objects.get(id=instance.id)
        if instance.thumbnail and not instance.image:
            this.image.delete(save=False)
            this.thumbnail.delete(save=False)
            instance.thumbnail.delete(save=False)
        elif not instance.thumbnail and this.thumbnail != instance.thumbnail:
            this.thumbnail.delete(save=False)
        elif this.image != instance.image:
            if this.image:
                this.image.delete(save=False)
            this.thumbnail.delete(save=False)
            create_thumbnail(instance)
    except ImageModel.DoesNotExist:
        create_thumbnail(instance)
