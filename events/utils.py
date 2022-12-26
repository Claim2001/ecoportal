import datetime

from rest_framework import serializers


def check_location(location):
    if location.keys() != {"geocode", "long", "lat"}:
        raise serializers.ValidationError(detail={"message": "Lat/long/geocode not in location"})
    if not isinstance(location['lat'], (float, int)):
        raise serializers.ValidationError(detail={"message": "Lat is not float or int"})
    if not isinstance(location['long'], (float, int)):
        raise serializers.ValidationError(detail={"message": "Long is not float or int"})
    if not isinstance(location['geocode'], str):
        raise serializers.ValidationError(detail={"message": "Geocode is not string"})


def update_location(location):
    for i in location:
        if i == "long" and not isinstance(location['long'], (float, int)):
            raise serializers.ValidationError(detail={"message": "Long is not float or int"})
        elif i == "lat" and not isinstance(location['lat'], (float, int)):
            raise serializers.ValidationError(detail={"message": "Lat is not float or int"})
        elif i == "geocode" and not isinstance(location['geocode'], str):
            raise serializers.ValidationError(detail={"message": "Geocode is not string"})
    else:
        pass


def update_working_hours(hours):
    try:
        for i in hours:
            if i == "opening":
                hours[i] = datetime.datetime.strptime(hours[i], '%H:%M').time()
            elif i == "closing":
                hours[i] = datetime.datetime.strptime(hours[i], '%H:%M').time()
            else:
                pass
    except Exception as e:
        raise serializers.ValidationError(detail={"message": e})
    return hours
