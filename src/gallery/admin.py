# pylint:disable=missing-class-docstring
from django.contrib import admin
from gallery.models import Gallery, ImageModel


class ImageModelInline(admin.TabularInline):
    model = ImageModel
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = (ImageModelInline,)


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    pass
