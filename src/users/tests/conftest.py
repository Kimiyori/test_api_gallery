import pytest
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def create_superuser():
    pytest.superuser = User.objects.create_superuser(
        email="test_admin@mail.ru", username="test_admin", password="test_admin"
    )
    token = RefreshToken.for_user(pytest.superuser)
    pytest.superuser.token = str(token.access_token)
    pytest.superuser.refresh = str(token)


@pytest.fixture
def create_user():
    pytest.user = User.objects.create_user(
        email="test@mail.ru", username="test", password="test"
    )
    token = RefreshToken.for_user(pytest.user)
    pytest.user.token = str(token.access_token)
    pytest.user.refresh = str(token)


@pytest.fixture
def create_user2():
    pytest.user2 = User.objects.create_user(
        email="test2@mail.ru", username="test2", password="test2"
    )
    token = RefreshToken.for_user(pytest.user2)
    pytest.user2.token = str(token.access_token)
    pytest.user2.refresh = str(token)
