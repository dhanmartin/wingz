from rest_framework import serializers
from rides.models import Ride, RideEvent
from users.models import User


class RideEventInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id', 'description', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='rider'))
    driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='driver'))

    todays_ride_events = RideEventInfoSerializer(many=True, source='ride_events', read_only=True)

    class Meta:
        model = Ride
        fields = "__all__"


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = "__all__"
