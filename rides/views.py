from datetime import timedelta
from django.db.models import Prefetch
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from rides.models import Ride, RideEvent
from rides.serializers import RideSerializer, RideEventSerializer
from users.permissions import IsAdminUserRole


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdminUserRole]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'rider__email': ['icontains'],
    }
    ordering_fields = ['pickup_time']
    ordering = ['pickup_time']

    def get_queryset(self):
        since = timezone.now() - timedelta(hours=24)
        qs = (
            Ride.objects.select_related('rider', 'driver')
            .prefetch_related(
                Prefetch(
                    'ride_events',
                    queryset=RideEvent.objects.filter(created_at__gte=since),
                )
            )
        )

        return qs


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUserRole]
