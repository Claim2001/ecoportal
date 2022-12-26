import datetime
import operator

from django.contrib.auth.models import User
from rest_framework import serializers, fields
from functools import reduce
from events.models import RecycleModel, RecycleImageModel, WORKING_DAYS, RECYCLE_TYPES
from events.serializers_violation import AuthorSerializer
from django.db.models import Q

from events.utils import check_location, update_location, update_working_hours


class RecycleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecycleImageModel
        fields = ['id', 'image', ]


class RecycleCreateSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(write_only=True, required=True)
    recycle_types = serializers.MultipleChoiceField(choices=RECYCLE_TYPES, required=True)
    working_days = serializers.MultipleChoiceField(choices=WORKING_DAYS, required=True)
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True), write_only=True)
    working_hours = serializers.JSONField(required=True, write_only=True)

    def validate(self, attrs):
        if not attrs['recycle_types']:
            raise serializers.ValidationError(detail={"message": "Recycle types not in data"})
        if not attrs['working_days']:
            raise serializers.ValidationError(detail={"message": "Working days not in data"})
        check_location(attrs['location'])
        update_working_hours(attrs['working_hours'])
        return attrs

    def create(self, validated_data):
        images = validated_data.pop('images')
        location = validated_data.pop('location')
        hours = validated_data.pop('working_hours')
        validated_data['opening'] = hours['opening']
        validated_data['closing'] = hours['closing']
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
        fields = ("name", "recycle_types", "working_days", "working_hours", "comment", "location", "images")


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
        fields = RecycleListSerializer.Meta.fields + ('can_change', 'comment')


class RecycleUpdateDeleteSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(required=False)
    author = AuthorSerializer()
    new_images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True),
                                       required=False, write_only=True)
    deleted_images = serializers.PrimaryKeyRelatedField(many=True, required=False, write_only=True,
                                                        queryset=RecycleImageModel.objects.all())
    images = RecycleImageSerializer(many=True, source='image')
    recycle_types = serializers.MultipleChoiceField(choices=RECYCLE_TYPES, required=False)
    working_days = serializers.MultipleChoiceField(choices=WORKING_DAYS, required=False)
    working_hours = serializers.JSONField(required=False)

    def validate(self, attrs):
        if 'working_hours' in attrs:
            update_working_hours(attrs['working_hours'])
        if 'location' in attrs:
            update_location(attrs['location'])
        return attrs

    def update(self, instance, validated_data):
        if 'new_images' in validated_data:
            new_images = validated_data.pop('new_images')
            for i in new_images:
                RecycleImageModel.objects.create(image=i, recycle=instance)

        if 'deleted_images' in validated_data:
            deleted_images = validated_data.pop('deleted_images')
            list_of_ids = []
            for d in deleted_images:
                list_of_ids.append(d.id)
            RecycleImageModel.objects.filter(id__in=list_of_ids, recycle=instance).delete()

        if 'working_hours' in validated_data:
            hours = validated_data.pop('working_hours')
            for i in hours:
                if i == 'opening':
                    validated_data['opening'] = hours[i]
                elif i == 'closing':
                    validated_data['closing'] = hours[i]
                else:
                    pass

        if 'location' in validated_data:
            location = validated_data.pop('location')
            for i in location:
                if i == "long":
                    validated_data['long'] = location['long']
                elif i == "lat":
                    validated_data['lat'] = location['lat']
                elif i == "geocode":
                    validated_data['geocode'] = location['geocode']
                else:
                    pass
        return super(RecycleUpdateDeleteSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(RecycleUpdateDeleteSerializer, self).to_representation(instance)
        data['location'] = {"lat": instance.lat, "long": instance.long, "geocode": instance.geocode}
        data['working_hours'] = {"opening": instance.opening, "closing": instance.closing}
        data['working_days'] = instance.get_working_days_display()
        data['recycle_types'] = instance.get_recycle_types_display()
        return data

    class Meta:
        model = RecycleModel
        fields = ('id', 'name', 'comment', 'location', 'author', 'new_images', 'deleted_images', 'images',
                  'recycle_types', 'working_days', 'working_hours')
        read_only_fields = ('id', 'author', 'images')
