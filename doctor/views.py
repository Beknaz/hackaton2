from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone

from .models import Doctor
from .serializers import DoctorSerializer
from permissions import IsAdminOrReadOnly, IsAuthor

class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['first_name', 'last_name']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('first_name', openapi.IN_QUERY, 'search doctors by name', type=openapi.TYPE_STRING)])

    @action(methods=['GET'], detail=False)
    def search(self, request):
        first_name = request.query_params.get('first_name')
        queryset = self.get_queryset()
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        
        serializer = DoctorSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)

    @action(methods=["GET"], detail=False)
    def order_by_rating(self, request):
        queryset = self.get_queryset()

        queryset = sorted(queryset, key=lambda doctor: doctor.average_rating, reverse=True)
        serializer = DoctorSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data, 200)



