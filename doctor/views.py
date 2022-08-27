from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Doctor, Category, ServiceListing, Comment, Like, Favorite, Rating, Chat, Entry
from .serializers import DoctorSerializer, CategorySerializer, ServiceListingSerializer, CommentSerializer, ChatSerializer, EntrySerializer, FavoriteSerializer
from permissions import IsAdminOrReadOnly, IsAuthor
from .tasks import entry_created

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


    @swagger_auto_schema(manual_parameters=[openapi.Parameter('categories', openapi.IN_QUERY, 'recomendations by categories', type=openapi.TYPE_STRING)])
    @action(methods=['GET'], detail=False)
    def recomendations(self, request):
        categories_title = request.query_params.get('categories')
        categories = Category.objects.get(title__icontains=categories_title)

        queryset = self.get_queryset()
        queryset = queryset.filter(categories=categories)
        
        queryset = max(queryset, key=lambda doctor: doctor.average_rating)
        serializer = DoctorSerializer(queryset, context={'request':request})
        return Response(serializer.data, 200)




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


class CategoryViewSet(mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin, 
                    GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceListingViewSet(mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin, 
                    GenericViewSet):
    queryset = ServiceListing.objects.all()
    serializer_class = ServiceListingSerializer
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor, IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def toggle_like(request, d_id):
    user = request.user
    doctor = get_object_or_404(Doctor, id=d_id)

    if Like.objects.filter(user=user, doctor=doctor).exists():
        Like.objects.filter(user=user, doctor=doctor).delete()
    else:
        Like.objects.create(user=user, doctor=doctor)
    return Response("Like toggled", 200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_rating(request, d_id):
    user = request.user
    doctor = get_object_or_404(Doctor, id=d_id)
    value = request.POST.get("value")

    if not value:
        raise ValueError("Value is required")

    if Rating.objects.filter(user=user, doctor=doctor, value=value).exists():
        rating = Rating.objects.get(user=user, doctor=doctor)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user, doctor=doctor, value=value)

    return Response("Rating created", 201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def add_to_favorites(request, d_id):
    user = request.user
    doctor = get_object_or_404(Doctor, id=d_id)

    if Favorite.objects.filter(user=user, doctor=doctor).exists():
        Favorite.objects.filter(user=user, doctor=doctor).delete()
    else:
        Favorite.objects.create(user=user, doctor=doctor)
    return Response("Added to favorites", 200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    queryset = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(queryset, many=True)
    return Response(serializer.data)


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class EntryViewSet(ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]

    
    def create(self, request, *args, **kwargs):
        r_data = request.data
        date = r_data["date"]
        time_slot = r_data["time_slot"]
        doctor = r_data["doctor"]
        entries = Entry.objects.filter(doctor=doctor)
        if entries:
            for e in entries:
                if str(e.date) == str(date) and str(e.time_slot) == str(time_slot):
                    return Response("This time slot is already booked for this doctor. Please choose another time or day")
        super().create(request, *args, **kwargs)
        entry = Entry.objects.get(date=date, time_slot=time_slot, doctor=doctor)
        entry_created.delay(entry.id)
        return Response("Appointment created")


    def update(self, request, *args, **kwargs):
        r_data = request.data
        date = r_data["date"]
        time_slot = r_data["time_slot"]
        entries = Entry.objects.filter(doctor=r_data["doctor"])
        if entries:
            for e in entries:
                if str(e.date) == str(date) and str(e.time_slot) == str(time_slot):
                    return Response("This time slot is already booked for this doctor. Please choose another time or day")
        return super().update(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
