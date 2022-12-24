from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    ListAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg import openapi

from events.models import RecycleModel, RecycleImageModel
from events.serializer_recycle import RecycleCreateSerializer, RecycleListSerializer, RecycleRetrieveSerializer


class RecycleCreateView(CreateAPIView):
    permissions = (permissions.IsAuthenticated,)
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleCreateSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Recycle is created"}, status=status.HTTP_201_CREATED)


class RecycleListView(ListAPIView):
    permissions = (permissions.IsAuthenticated, )
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleListSerializer


class RecycleRetrieveView(RetrieveAPIView):
    permissions = (permissions.IsAuthenticated, )
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleRetrieveSerializer
    lookup_url_kwarg = 'id'
