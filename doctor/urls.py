from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DoctorViewSet, CommentViewSet, CategoryViewSet, ServiceListingViewSet, EntryViewSet, ChatViewSet, add_to_favorites, toggle_like, add_rating

router = DefaultRouter()
router.register("doctor", DoctorViewSet)
router.register("categories", CategoryViewSet)
router.register("comments", CommentViewSet)
router.register("service_listing", ServiceListingViewSet)
router.register("entries", EntryViewSet)
router.register("chats", ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('toggle_like/<int:d_id>/', toggle_like),
    path('add_rating/<int:d_id>/', add_rating),
    path('add_to_favorites/<int:d_id>/', add_to_favorites),
]