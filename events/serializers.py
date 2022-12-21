from django.contrib.auth.models import User
from rest_framework import serializers

from events.models import ViolationModel, ViolationImageModel, TITLES


class AuthorSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True, source='profile.avatar')

    class Meta:
        model = User
        fields = ['id', 'avatar']


class ViolationCreateSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True))
    location = serializers.JSONField()
    title = serializers.ChoiceField(choices=TITLES)
    comment = serializers.CharField()

    def validate(self, attrs):
        if attrs['location'].keys() != {"geocode", "long", "lat"}:
            raise serializers.ValidationError(detail={"message":"Lat/long/geocode not in location"})
        return attrs


class ViolationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationImageModel
        fields = ['id', 'image', ]


class ViolationListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        return {"lat": obj.lat, "long": obj.long, "geocode": obj.geocode}

    def get_author(self, obj):
        return AuthorSerializer(obj.author, many=False, context=self.context).data

    def get_image(self, obj):
        return ViolationImageSerializer(
            ViolationImageModel.objects.filter(violation=obj).order_by('-created_at').first(), many=False,
            context=self.context).data['image']

    class Meta:
        model = ViolationModel
        fields = ['id', 'image', 'author', 'location']


class ViolationRetrieveSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    images = ViolationImageSerializer(many=True, source='image')

    def to_representation(self, instance):
        data = super(ViolationRetrieveSerializer, self).to_representation(instance)
        data['location'] = {"lat": data.pop('lat'), "long": data.pop('long'), "geocode": data.pop('geocode')}
        user = self.context['request'].user
        data['can_change'] = True if instance.author == user or user.is_superuser else False
        data['title'] = instance.get_title_display()
        return data

    class Meta:
        model = ViolationModel
        fields = ['id', 'title', 'author', 'lat', 'geocode', 'long', 'images']


class ViolationUpdateDeleteSerializer(serializers.ModelSerializer):
    location = serializers.JSONField(required=False)
    author = AuthorSerializer()
    new_images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False, use_url=True),
                                       required=False, write_only=True)
    deleted_images = serializers.PrimaryKeyRelatedField(many=True, required=False, write_only=True,
                                                        queryset=ViolationImageModel.objects.all())
    images = ViolationImageSerializer(many=True, source='image')

    def update(self, instance, validated_data):
        if 'new_images' in validated_data:
            new_images = validated_data.pop('new_images')
            for i in new_images:
                ViolationImageModel.objects.create(image=i, violation=instance)

        if 'deleted_images' in validated_data:
            deleted_images = validated_data.pop('deleted_images')
            list_of_ids = []
            for d in deleted_images:
                list_of_ids.append(d.id)
            ViolationImageModel.objects.filter(id__in=list_of_ids, violation=instance).delete()

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
        return super(ViolationUpdateDeleteSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(ViolationUpdateDeleteSerializer, self).to_representation(instance)
        data['location'] = {"lat": data.pop('lat'), "long": data.pop('long'), "geocode": data.pop('geocode')}
        user = self.context['request'].user
        data['title'] = instance.get_title_display()
        return data

    class Meta:
        model = ViolationModel
        fields = ['id', 'title', 'comment', 'author', 'lat', 'long', 'location', 'geocode', 'images', 'deleted_images',
                  'new_images']
        read_only_fields = ('id', 'author', 'lat', 'long', 'geocode', 'images')
