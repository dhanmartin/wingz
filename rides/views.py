from datetime import timedelta
from django.db.models import Prefetch
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from django.db.models import F, FloatField, ExpressionWrapper, Value

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
    ordering_fields = ['pickup_time', 'distance']
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

        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        distance_expression = None
        if lat and lng:
            try:
                lat = float(lat)
                lng = float(lng)
                distance_expression = ((F('pickup_latitude') - lat) ** 2 + (F('pickup_longitude') - lng) ** 2) ** 0.5
            except ValueError:
                pass # Ignore invalid lat/lng

        if distance_expression is not None:
            qs = (
                qs.filter(pickup_latitude__isnull=False, pickup_longitude__isnull=False)
                .annotate(
                    distance=ExpressionWrapper(distance_expression, output_field=FloatField())
                )
            )
        else:
            qs = qs.annotate(distance=ExpressionWrapper(Value(0), output_field=FloatField()))

        return qs


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUserRole]
