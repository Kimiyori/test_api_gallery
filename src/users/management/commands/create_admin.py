from typing import Any
from users.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        username = "test_admin"
        password = "test_admin"
        email = "test_admin@gmail.com"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, password=password, email=email
            )
