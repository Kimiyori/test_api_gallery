from rest_framework import serializers, validators
from django.contrib.auth.models import AbstractBaseUser
from users.models import User
from users.services.db_services import create_user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for safe methods"""

    class Meta:  # pylint: disable=missing-class-docstring
        model = User
        fields = ("id", "username", "email")


class UserRegSerializer(serializers.ModelSerializer):
    """Serialiser for user registration or update"""

    password = serializers.CharField(write_only=True)

    class Meta:  # pylint: disable=missing-class-docstring
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with same email already exists",
                    )
                ],
            },
        }

    def create(self, validated_data: dict[str, str | int]) -> AbstractBaseUser:
        """
        Handles the validated data to create a user.
        """
        user: AbstractBaseUser = create_user(validated_data)
        return user

    def update(
        self, instance: AbstractBaseUser, validated_data: dict[str, str]
    ) -> AbstractBaseUser:
        """
        Handles the validated data to update a user.
        """
        if validated_data.get("password"):
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)  # type:ignore
