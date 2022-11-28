import pytest
from pathlib import Path
from gallery.models import ImageModel, image_path
from gallery.services.image_services import generate_gallery_path
from gallery.tests.conftest import (
    create_gallery,
    TEST_DIR,
    get_temporary_image,
    image_folder,
)


@pytest.mark.usefixtures("create_gallery", "image_folder")
@pytest.mark.django_db
def test_create_image_instance(get_temporary_image):
    image = ImageModel.objects.create(gallery=pytest.gallery, image=get_temporary_image)
    assert image.image.name.split("/")[-1] == get_temporary_image.name
    assert image.thumbnail.name.split("/")[-1] == get_temporary_image.name
    path_original_obj = Path(image.image.path)
    path_thumbnail_obj = Path(image.thumbnail.path)
    assert path_original_obj.exists()
    assert path_thumbnail_obj.exists()


@pytest.mark.usefixtures("create_gallery", "image_folder")
@pytest.mark.django_db
def test_delete_image(get_temporary_image):
    image = ImageModel.objects.create(gallery=pytest.gallery, image=get_temporary_image)
    path_original_obj = Path(image.image.path)
    path_thumbnail_obj = Path(image.thumbnail.path)
    image.image.delete()
    assert not image.image
    assert not image.thumbnail
    assert not path_original_obj.exists()
    assert not path_thumbnail_obj.exists()


@pytest.mark.usefixtures("create_gallery", "image_folder")
@pytest.mark.django_db
def test_delete_thumbnail(get_temporary_image):
    image = ImageModel.objects.create(gallery=pytest.gallery, image=get_temporary_image)
    path_original_obj = Path(image.image.path)
    path_thumbnail_obj = Path(image.thumbnail.path)
    image.thumbnail.delete()
    assert image.image
    assert not image.thumbnail
    assert path_original_obj.exists()
    assert not path_thumbnail_obj.exists()


@pytest.mark.usefixtures("create_gallery", "image_folder")
@pytest.mark.django_db
def test_delete_image_instance(get_temporary_image):
    image = ImageModel.objects.create(gallery=pytest.gallery, image=get_temporary_image)
    path_original_obj = Path(image.image.path)
    path_thumbnail_obj = Path(image.thumbnail.path)
    image.delete()
    assert not path_original_obj.exists()
    assert not path_thumbnail_obj.exists()


@pytest.mark.usefixtures("create_gallery", "image_folder")
@pytest.mark.django_db
def test_delete_gallery(get_temporary_image):
    path_gallery = Path(generate_gallery_path(pytest.gallery))
    ImageModel.objects.create(gallery=pytest.gallery, image=get_temporary_image)
    assert path_gallery.exists()
    pytest.gallery.delete()
    assert not path_gallery.exists()
