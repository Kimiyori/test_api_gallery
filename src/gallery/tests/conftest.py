import shutil
import pytest
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as ImageTest
from io import BytesIO
from gallery.models import Gallery
from users.tests.conftest import create_user

TEST_DIR = "test_data"


@pytest.fixture
def create_gallery(create_user):
    pytest.gallery = Gallery.objects.create(name="test", user=pytest.user)


@pytest.fixture
def get_temporary_image():
    """Create temporary file for test"""
    temp_file = BytesIO()
    size = (1000, 1000)
    color = (255, 0, 0, 0)
    image = ImageTest.new("RGBA", size, color)
    image.save(temp_file, "png")
    temp_file.seek(0)
    return SimpleUploadedFile(f"test.jpg", temp_file.getvalue())


@pytest.fixture
def image_folder():
    yield
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
