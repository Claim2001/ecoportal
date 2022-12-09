from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from PIL import Image
from io import BytesIO
import os
from django.core.files import File

from events.models import ViolationModel, ViolationImageModel
from events.serializers import ViolationCreateSerializer


def get_resize_image_or_none(image, size, format=None):
    im = Image.open(image)
    im.thumbnail(size, Image.ANTIALIAS)
    filename = os.path.basename(image.name)
    basename = os.path.splitext(filename)[0]
    if format in ['jpeg', 'png', 'bmp'] and format != im.format:
        im = im.convert('RGB')
    else:
        format = im.format.lower()
    thumb_io = BytesIO()
    im.save(thumb_io, format)
    return File(thumb_io, name=basename + '.' + format)


class ViolationCreateView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ViolationCreateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        images = self.request.FILES.getlist('images')
        vm = ViolationModel.objects.create(title=data['title'], lat=data['lat'], long=data['long'],
                                           comment=data['comment'])
        for image in images:
            ViolationImageModel.objects.create(violation=vm, image=image)
        return Response({"message": "Violation is created"}, status=status.HTTP_201_CREATED)
