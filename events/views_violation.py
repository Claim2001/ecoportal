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
    """
        List of violations
            Response: 200 - [{"id":int,"images":[{"id":int,"image":url_to_image},...], "title":string,
            "author":{"id":int,"avatar":ulr_to_image},"location":{"lat":float,"long":float,"geocode":string},},...]
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ViolationListSerializer
    queryset = ViolationModel.objects.all()


class ViolationRetrieveView(RetrieveAPIView):
    """
        Get violation detail
            Response: 200 - {"id":int,"title":string","author":{"id":int,"avatar":url_to_image},"can_change":bool,
            "location":{"lat":float,"long":float,"geocode":string},"images":[{"id":int,"image":url_to_image},...]}
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ViolationRetrieveSerializer
    queryset = ViolationModel.objects.all()
    lookup_url_kwarg = 'id'


class ViolationUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    """
        Update/Delete violation
            Can be performed only by author or superuser
            For update better use PATCH method(no need for sending all data in body, only changed one):
                Body: {"title":int,"comment":string,"location":{"lat":float,"long":float,"geocode":string},
                "deleted_images":[int,int,int,...],"new_images":[FILE(image type),FILE(image type),...]}
                Titles: 1 - Illegal Dump, 2 - Deforestation, 3 - Water Pollution
                Deleted images: list of ids of images that user have chosen to delete
                Response: 200 - {"id":int,"title":string,"comment":string,"author":{"id":int,"avatar":ulr_to_image},
                "images":[{"id":int,"image":url_to_image},...],"location":{"lat":float,"long":float,"geocode":string}}
            For delete use DELETE method
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ViolationUpdateDeleteSerializer
    queryset = ViolationModel.objects.all()
    lookup_url_kwarg = 'id'

    def update(self, request, *args, **kwargs):
        if self.request.user != self.get_object().author and not self.request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super(ViolationUpdateDeleteView, self).update(request, *args, **kwargs)
