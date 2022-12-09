from rest_framework import serializers

from events.models import ViolationModel


class ViolationCreateSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True))
    lat = serializers.FloatField()
    long = serializers.FloatField()
    title = serializers.CharField()
    comment = serializers.CharField()
