from rest_framework import viewsets
from rides.models import Ride, RideEvent
from rides.serializers import RideSerializer, RideEventSerializer
from users.permissions import IsAdminUserRole

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUserRole]


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUserRole]
