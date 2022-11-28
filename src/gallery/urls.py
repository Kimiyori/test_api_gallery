from rest_framework.routers import SimpleRouter
from gallery.views import GalleryViewSet, AdminGallery

router = SimpleRouter(trailing_slash=False)
router.register(r"", GalleryViewSet, basename="gallery")
router.register(r"admin", AdminGallery, basename="admin")
urlpatterns = []
urlpatterns += router.urls
