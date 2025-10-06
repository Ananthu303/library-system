from rest_framework.routers import DefaultRouter
from .views import BookViewSet,LendingViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("lend-books", LendingViewSet, basename="lend-books")

urlpatterns = router.urls
