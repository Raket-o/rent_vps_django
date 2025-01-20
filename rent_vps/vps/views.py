from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .models import VPS
from .serializers import VPSSerializer


class VPSViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", ]
    queryset = VPS.objects.all()
    serializer_class = VPSSerializer
    fields = ["id", "uid", "cpu", "ram", "hdd", "status"]

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = fields
    filterset_fields = fields
    ordering_fields = fields

    def partial_update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        if data.get("status") and instance.status != data.get("status"):
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data="it is allowed to change only the server status.",
                status=status.HTTP_400_BAD_REQUEST
            )
