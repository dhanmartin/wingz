from rest_framework.routers import DefaultRouter
from rides.views import RideViewSet, RideEventViewSet

router = DefaultRouter()
router.register(r"rides", RideViewSet, basename="ride")
router.register(r"ride-events", RideEventViewSet, basename="ride-event")

urlpatterns = router.urls
