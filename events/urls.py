from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import (
    EventViewSet,
    AttendanceViewSet
)

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')
router.register('attendances', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]