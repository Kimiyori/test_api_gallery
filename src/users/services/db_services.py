from users.models import User


def create_user(data: dict[str, str]) -> User:
    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    return user
