# pylint: disable=missing-class-docstring,import-outside-toplevel,unused-import
from django.apps import AppConfig


class GalleryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gallery"

    def ready(self) -> None:
        from gallery import signals  # noqa: F401
