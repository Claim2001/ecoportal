from django.contrib.auth.models import User
from rest_framework import serializers

from events.models import ChargingStationModel, ChargingStationImageModel, PAYMENT_METHODS, CHARGING_TYPES
from events.serializers_violation import AuthorSerializer
from events.utils import check_location, update_location


class StationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStationImageModel
        fields = ('id', 'image',)


class StationCreateSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(write_only=True, required=True)
    payment_method = serializers.MultipleChoiceField(choices=PAYMENT_METHODS, required=True)
    charging_type = serializers.ChoiceField(choices=CHARGING_TYPES, required=True)
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True), write_only=True)

    def validate(self, attrs):
        if 'payment_method' not in attrs or not attrs['payment_method']:
            raise serializers.ValidationError(detail={"message": "Payment method not in data"})
        check_location(attrs['location'])
        return attrs

    def create(self, validated_data):
        images = validated_data.pop('images')
        location = validated_data.pop('location')
        validated_data['lat'] = location['lat']
        validated_data['long'] = location['long']
        validated_data['geocode'] = location['geocode']
        validated_data['author'] = self.context['request'].user
        recycle = super(StationCreateSerializer, self).create(validated_data)
        for i in images:
            ChargingStationImageModel.objects.create(station=recycle, image=i)
        return validated_data

    class Meta:
        model = ChargingStationModel
        fields = ('title', 'price', 'payment_method', 'charging_type', 'description', 'images', 'location')


class StationListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    images = StationImageSerializer(many=True, source='image')
    payment_method = serializers.SerializerMethodField()
    author = AuthorSerializer()
    charging_type = serializers.SerializerMethodField()

    def get_payment_method(self, obj):
        return obj.get_payment_method_display()

    def get_charging_type(self, obj):
        return obj.get_charging_type_display()

    def get_location(self, obj):
        return {"lat": obj.lat, "long": obj.long, "geocode": obj.geocode}

    class Meta:
        model = ChargingStationModel
        fields = ('id', 'title', 'price', 'location', 'images', 'payment_method', 'charging_type', 'author')


class StationRetrieveSerializer(StationListSerializer):
    can_change = serializers.SerializerMethodField()

    def get_can_change(self, obj):
        user = self.context['request'].user
        return True if (obj.author == user or user.is_superuser) else False

    class Meta(StationListSerializer.Meta):
        model = ChargingStationModel
        fields = StationListSerializer.Meta.fields + ('can_change', 'description')


class StationUpdateDeleteSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(required=False)
    author = AuthorSerializer()
    new_images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True),
                                       required=False, write_only=True)
    deleted_images = serializers.PrimaryKeyRelatedField(many=True, required=False, write_only=True,
                                                        queryset=ChargingStationImageModel.objects.all())
    images = StationImageSerializer(many=True, source='image')
    payment_method = serializers.MultipleChoiceField(choices=PAYMENT_METHODS, required=False)
    charging_type = serializers.ChoiceField(choices=CHARGING_TYPES, required=False)

    def validate(self, attrs):
        if 'location' in attrs:
            update_location(attrs['location'])
        return attrs

    def update(self, instance, validated_data):
        if 'new_images' in validated_data:
            new_images = validated_data.pop('new_images')
            for i in new_images:
                ChargingStationImageModel.objects.create(image=i, station=instance)

        if 'deleted_images' in validated_data:
            deleted_images = validated_data.pop('deleted_images')
            list_of_ids = []
            for d in deleted_images:
                list_of_ids.append(d.id)
            ChargingStationImageModel.objects.filter(id__in=list_of_ids, station=instance).delete()

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
        return super(StationUpdateDeleteSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(StationUpdateDeleteSerializer, self).to_representation(instance)
        data['location'] = {"lat": instance.lat, "long": instance.long, "geocode": instance.geocode}
        data['payment_method'] = instance.get_payment_method_display()
        data['charging_type'] = instance.get_charging_type_display()
        return data

    class Meta:
        model = ChargingStationModel
        fields = ('id', 'title', 'price', 'description', 'location', 'author', 'new_images', 'deleted_images', 'images',
                  'payment_method', 'charging_type')
        read_only_fields = ('id', 'author', 'images')
