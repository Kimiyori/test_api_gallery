# pylint: disable=missing-class-docstring
from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer

from gallery.models import Gallery, ImageModel


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ("id", "image", "thumbnail")


class GallerySerializer(serializers.ModelSerializer):
    images = ImageModelSerializer(
        many=True,
    )
    user = UserSerializer()

    class Meta:
        model = Gallery
        fields = ("id", "user", "name", "images")


class GalleryNotSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ("id", "name")

    def create(self, validated_data: dict[str, str | int]) -> Gallery:
        user, _ = User.objects.get_or_create(id=validated_data.pop("user_id"))
        gallery = Gallery.objects.create(  # pylint: disable=no-member
            user=user, name=validated_data.pop("name")
        )
        return gallery


class GalleryUploadImageSerializer(serializers.Serializer):
    image=serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False)
