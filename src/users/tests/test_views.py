import json
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework import status
import pytest
from users.views import RegisterViewSet
from users.models import User


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_get_user_me(client):
    url = reverse("user-me")
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    response = client.get(url, **headers)
    assert response.status_code == status.HTTP_200_OK
    assert int(response.data["id"]) == pytest.user.id
    assert response.data["username"] == pytest.user.username


def test_get_user_me_not_auth(client):
    url = reverse("user-me")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_post_user(client):
    url = reverse("user-list")
    data = {"username": "test", "email": "test@mail.ru", "password": "test"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(pk=response.data["id"])
    assert user.email == data["email"]


@pytest.mark.django_db
def test_post_user_not_full(client):
    url = reverse("user-list")
    data = {"username": "test", "email": "test@mail.ru"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_delete_user(client):
    pk = pytest.user.id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    url = reverse("user-detail", args=[pk])
    response = client.delete(url, **headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    user = User.objects.filter(pk=pk)
    assert not user


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_delete_user_not_owner(client):
    user = User.objects.create_user(
        email="test2@mail.ru", username="test2", password="test2"
    )
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    url = reverse("user-detail", args=[user.pk])
    response = client.delete(url, **headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_put_user(client):
    pk = pytest.user.id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    data = {"username": "test", "email": "test@mail.ru", "password": "te1st"}
    url = reverse("user-detail", args=[pk])
    response = client.put(
        url, json.dumps(data), content_type="application/json", **headers
    )
    assert response.status_code == status.HTTP_200_OK
    user = User.objects.get(pk=pk)
    assert check_password(data["password"], user.password)


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_get_user(client):
    pk = pytest.user.id
    headers = {"HTTP_AUTHORIZATION": f"Bearer {pytest.user.token}"}
    url = reverse("user-detail", args=[pk])
    response = client.get(url, **headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
