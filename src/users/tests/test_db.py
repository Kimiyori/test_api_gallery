import pytest

from users.models import User


@pytest.mark.usefixtures("create_user")
@pytest.mark.django_db
def test_user():
    user = User.objects.get(id=pytest.user.id)
    assert user.is_superuser == False
    assert user.is_staff == False
    assert user.is_admin == False
    assert user.is_active == True


@pytest.mark.usefixtures("create_superuser")
@pytest.mark.django_db
def test_superuser():
    user = User.objects.get(id=pytest.superuser.id)
    assert user.is_superuser == True
    assert user.is_staff == True
    assert user.is_admin == True
    assert user.is_active == True
