from rest_framework.routers import SimpleRouter
from gallery.views import GalleryViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"", GalleryViewSet, basename="gallery")

urlpatterns = []
urlpatterns += router.urls
