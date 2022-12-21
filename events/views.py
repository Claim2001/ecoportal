from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    ListAPIView
from rest_framework.response import Response
from drf_yasg import openapi

from events.models import ViolationModel, ViolationImageModel
from events.serializers import ViolationCreateSerializer, ViolationRetrieveSerializer, \
    ViolationListSerializer, ViolationUpdateDeleteSerializer


class ViolationCreateView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=ViolationCreateSerializer,
                         responses={201: openapi.Response(description="Violation is created"),
                                    400: openapi.Response(description="Lat/long/geocode not in location")})
    def post(self, request, *args, **kwargs):
        """
            Registration API
                Body: {"images": FILE(type of image, 1 or more), "title": int(1, 2 or 3), "comment": string,
                "location":{"lat": float, "long": float, "geocode": string}}
                Titles: 1 - Illegal Dump, 2 - Deforestation, 3 - Water Pollution
                Responses: 201 - {"message": "Violation is created"}
                            400 - {"message": "Lat/long/geocode not in location"}
        """
        serializer = ViolationCreateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        images = self.request.FILES.getlist('images')
        location = data['location']
        vm = ViolationModel.objects.create(title=data['title'], lat=location['lat'], long=location['long'],
                                           geocode=location['geocode'], comment=data['comment'],
                                           author=self.request.user)
        for image in images:
            ViolationImageModel.objects.create(violation=vm, image=image)
        return Response({"message": "Violation is created"}, status=status.HTTP_201_CREATED)


class ViolationListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ViolationListSerializer
    queryset = ViolationModel.objects.all()


class ViolationRetrieveView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ViolationRetrieveSerializer
    queryset = ViolationModel.objects.all()
    lookup_url_kwarg = 'id'


class ViolationUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ViolationUpdateDeleteSerializer
    queryset = ViolationModel.objects.all()
    lookup_url_kwarg = 'id'

    def update(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author and not self.request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super(ViolationUpdateDeleteView, self).update(request, *args, **kwargs)
