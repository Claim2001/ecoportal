import datetime
import operator

from django.contrib.auth.models import User
from rest_framework import serializers, fields
from functools import reduce
from events.models import RecycleModel, RecycleImageModel, WORKING_DAYS, RECYCLE_TYPES
from events.serializers_violation import AuthorSerializer
from django.db.models import Q


class RecycleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecycleImageModel
        fields = ['id', 'image', ]


class RecycleCreateSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(write_only=True)
    recycle_types = serializers.MultipleChoiceField(choices=RECYCLE_TYPES, required=True)
    working_days = serializers.MultipleChoiceField(choices=WORKING_DAYS, required=True)
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True), write_only=True)

    def validate(self, attrs):
        if not attrs['recycle_types']:
            raise serializers.ValidationError(detail={"message": "Recycle types not in data"})
        if not attrs['working_days']:
            raise serializers.ValidationError(detail={"message": "Working days not in data"})
        if attrs['location'].keys() != {"geocode", "long", "lat"}:
            raise serializers.ValidationError(detail={"message": "Lat/long/geocode not in location"})
        if not isinstance(attrs['location']['lat'], (float, int)):
            raise serializers.ValidationError(detail={"message": "Lat is not float or int"})
        if not isinstance(attrs['location']['long'], (float, int)):
            raise serializers.ValidationError(detail={"message": "Long is not float or int"})
        if not isinstance(attrs['location']['geocode'], str):
            raise serializers.ValidationError(detail={"message": "Geocode is not string"})
        return attrs

    def create(self, validated_data):
        images = validated_data.pop('images')
        location = validated_data.pop('location')
        validated_data['lat'] = location['lat']
        validated_data['long'] = location['long']
        validated_data['geocode'] = location['geocode']
        validated_data['author'] = self.context['request'].user
        recycle = super(RecycleCreateSerializer, self).create(validated_data)
        for i in images:
            RecycleImageModel.objects.create(recycle=recycle, image=i)
        return validated_data

    class Meta:
        model = RecycleModel
        fields = ("name", "recycle_types", "working_days", "opening", "closing", "comment", "location", "images")


class RecycleListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    images = RecycleImageSerializer(many=True, source='image')
    recycle_types = serializers.SerializerMethodField()
    working_days = serializers.SerializerMethodField()
    author = AuthorSerializer()
    working_hours = serializers.SerializerMethodField()

    def get_working_hours(self, obj):
        return {"opening": obj.opening, "closing": obj.closing}

    def get_working_days(self, obj):
        return obj.get_working_days_display()

    def get_recycle_types(self, obj):
        return obj.get_recycle_types_display()

    def get_location(self, obj):
        return {"lat": obj.lat, "long": obj.long, "geocode": obj.geocode}

    class Meta:
        model = RecycleModel
        fields = ('id', 'name', 'location', 'images', 'recycle_types', 'working_days', 'author', 'working_hours')


class RecycleRetrieveSerializer(RecycleListSerializer):
    can_change = serializers.SerializerMethodField()

    def get_can_change(self, obj):
        user = self.context['request'].user
        return True if (obj.author == user or user.is_superuser) else False

    class Meta(RecycleListSerializer.Meta):
        model = RecycleModel
        fields = RecycleListSerializer.Meta.fields + ('can_change',)
