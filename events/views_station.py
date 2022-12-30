from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    ListAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg import openapi

from events.models import ChargingStationModel
from events.serializer_station import StationCreateSerializer, StationListSerializer, StationRetrieveSerializer, \
    StationUpdateDeleteSerializer


class StationCreateView(CreateAPIView):
    permissions = (permissions.IsAuthenticated,)
    queryset = ChargingStationModel.objects.all()
    serializer_class = StationCreateSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Charging station is created"}, status=status.HTTP_201_CREATED)


class StationListView(ListAPIView):
    permissions = (permissions.IsAuthenticated,)
    queryset = ChargingStationModel.objects.all()
    serializer_class = StationListSerializer


class StationRetrieveView(RetrieveAPIView):
    permission = (permissions.IsAuthenticated,)
    queryset = ChargingStationModel.objects.all()
    serializer_class = StationRetrieveSerializer
    lookup_url_kwarg = 'id'


class StationUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    permissions = (permissions.IsAuthenticated,)
    queryset = ChargingStationModel.objects.all()
    serializer_class = StationUpdateDeleteSerializer
    lookup_url_kwarg = 'id'

    def get_object(self):
        obj = get_object_or_404(ChargingStationModel, id=self.kwargs['id'])
        if self.request.user != obj.author and not self.request.user.is_superuser:
            raise Http404
        return obj
