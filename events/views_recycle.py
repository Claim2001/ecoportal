from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    ListAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg import openapi

from events.models import RecycleModel, RecycleImageModel
from events.serializer_recycle import RecycleCreateSerializer, RecycleListSerializer, RecycleRetrieveSerializer, \
    RecycleUpdateDeleteSerializer


class RecycleCreateView(CreateAPIView):
    permissions = (permissions.IsAuthenticated,)
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleCreateSerializer

    def create(self, request, *args, **kwargs):
        """
            Create Recycle
                Body: {"name":string, "recycle_types": [int, int, ...], "working_days": [int, int, ...],
                "working_hours": {"opening": "09:30", "closing": "22:00"}, "images": FILE(type of image, 1 or more),
                "comment": string, "location":{"lat": float, "long": float, "geocode": string}}
                Recycle Types: 1 - Scrap metal(Металлолом), 2 - Waste paper(Макулатура), 3 - Glass(Стекло),
                4 - Mechanism(Техника), 5 - Furniture(Мебель), 6 - Plastic(Пластик)
                Working Days: 1 - Monday, 2 - Tuesday, etc. till 7 - Sunday
                Responses: 201 - {"message": "Recycle is created"}
        """
        super().create(request, *args, **kwargs)
        return Response({"message": "Recycle is created"}, status=status.HTTP_201_CREATED)


class RecycleListView(ListAPIView):
    """
        List of recycles
            Response: 200 - [{"id":int,"name":string, "recycle_types": "string, string, ...",
            "working_days": "string, string, ...", "images":[{"id":int,"image":url_to_image},...],
            "working_hours": {"opening": "hour:minute", "closing": "hour:minute",
            "author":{"id":int,"avatar":ulr_to_image}, "location":{"lat":float,"long":float,"geocode":string},},...]
    """
    permissions = (permissions.IsAuthenticated,)
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleListSerializer


class RecycleRetrieveView(RetrieveAPIView):
    """
        Get recycle detail
            Response: 200 - {"id":int,"name":string","author":{"id":int,"avatar":url_to_image},"can_change":bool,
            "location":{"lat":float,"long":float,"geocode":string},"images":[{"id":int,"image":url_to_image},...],
            "working_days": "string, string, ...", "working_hours": {"opening": "hour:minute", "closing": "hour:minute",
            "recycle_types": "string, string, ..."}
    """
    permissions = (permissions.IsAuthenticated,)
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleRetrieveSerializer
    lookup_url_kwarg = 'id'


class RecycleUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    """
        Update/Delete recycle
            Can be performed only by author or superuser
            For update better use PATCH method(no need for sending all data in body, only the changed one):
                Body: {"name":string, "recycle_types": [int, int, ...], "working_days": [int, int, ...],
                "working_hours": {"opening": "09:30", "closing": "22:00"}, "comment": string,
                "location":{"lat": float, "long": float, "geocode": string}, "deleted_images":[int,int,int,...],
                "new_images":[FILE(image type),FILE(image type),...]}
                Recycle Types: 1 - Scrap metal(Металлолом), 2 - Waste paper(Макулатура), 3 - Glass(Стекло),
                4 - Mechanism(Техника), 5 - Furniture(Мебель), 6 - Plastic(Пластик)
                Working Days: 1 - Monday, 2 - Tuesday, etc. till 7 - Sunday
                Deleted images: list of ids of images that user have chosen to delete
                Response: 200 - {"id":int,"name":string","author":{"id":int,"avatar":url_to_image},"can_change":bool,
                "location":{"lat":float,"long":float,"geocode":string},"images":[{"id":int,"image":url_to_image},...],
                "working_days": "string, string, ...", "working_hours": {"opening": "hour:minute",
                "closing": "hour:minute", "recycle_types": "string, string, ..."}
            For delete use DELETE method
    """
    permissions = (permissions.IsAuthenticated,)
    queryset = RecycleModel.objects.all()
    serializer_class = RecycleUpdateDeleteSerializer
    lookup_url_kwarg = 'id'

    def get_object(self):
        obj = get_object_or_404(RecycleModel, id=self.kwargs['id'])
        if self.request.user != obj.author and not self.request.user.is_superuser:
            raise Http404
        return obj
