import json
import pytest
from gallery.models import Gallery
from users.tests.conftest import create_user, create_user2
from django.urls import reverse
from rest_framework import status
from django.test.client import MULTIPART_CONTENT
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_create_gallery_api(client):
    url = reverse("gallery-list")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    data = {"name": "test"}
    response = client.post(url, data, **headers)
    assert response.status_code == status.HTTP_201_CREATED
    gallery = Gallery.objects.filter(id=response.data["id"])
    assert gallery[0].name == data["name"]


@pytest.mark.usefixtures("create_user", "create_gallery")
@pytest.mark.django_db
def test_get_gallery_api(client):
    url = reverse("gallery-detail", args=[pytest.gallery.id])
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    response = client.get(url, **headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["id"] == pytest.gallery.user.id
    assert response.data["name"] == pytest.gallery.name


@pytest.mark.usefixtures("create_user", "create_gallery")
@pytest.mark.django_db
def test_put_gallery_api(client):
    url = reverse("gallery-detail", args=[pytest.gallery.id])
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    data = {"name": "test_change"}
    response = client.put(
        url, json.dumps(data), content_type="application/json", **headers
    )
    assert response.status_code == status.HTTP_200_OK
    gallery = Gallery.objects.filter(id=pytest.gallery.id)
    assert gallery[0].name == data["name"]


@pytest.mark.usefixtures("create_user2", "create_gallery")
@pytest.mark.django_db
def test_put_gallery_api_wrong_owner(client):
    url = reverse("gallery-detail", args=[pytest.gallery.id])
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user2.token}"}
    data = {"name": "test_change"}
    response = client.put(
        url, json.dumps(data), content_type="application/json", **headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.usefixtures("create_user", "create_gallery")
@pytest.mark.django_db
def test_delete_gallery_api(client):
    url = reverse("gallery-detail", args=[pytest.gallery.id])
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    response = client.delete(url, **headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.usefixtures("create_user", "create_gallery")
@pytest.mark.django_db
def test_upload_image_api(client, get_temporary_image):
    url = reverse("gallery-upload-image", args=[pytest.gallery.id])
    data = {"image": get_temporary_image}
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    response = client.post(url, data, content_type=MULTIPART_CONTENT, **headers)
    assert response.status_code == status.HTTP_200_OK
