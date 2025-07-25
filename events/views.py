from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from events.utils import CustomPagination
from events.serializers import EventSerializer, AttendanceSerializer
from events.models import Event, Attendance


class EventViewSet(ModelViewSet):
    """
    ViewSet to handle CRUD operations for events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update', 'view_my_events']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def list(self, request, *args, **kwargs):
        """
        List all events with pagination.
        """        
        queryset = self.get_queryset()
        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(location__icontains=q) |
                Q(key_words__icontains=q)
            )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

    def create(self, request, *args, **kwargs):
        if request.user.user_type != "organizer":
            return Response({
                "response": 1,
                "message": "You do not have permission to create events.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        event.organizer = request.user
        event.save()
        if not event:
            return Response({
                "response": 1,
                "message": "Event creation failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            "response": 0,
            "message": "Event created successfully.",
            "event": EventSerializer(event).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user.user_type != "organizer" or request.user != instance.organizer:
            return Response({
                "response": 1,
                "message": "You do not have permission to update events.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        return Response({
            "response": 0,
            "message": "Event updated successfully.",
            "event": EventSerializer(event).data
        }, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def view_my_events(self, request):
        """
        View all events created by the authenticated user.
        """
        if request.user.user_type != "organizer":
            events = Event.objects.filter(attendances__user=request.user)
        else:   
            events = Event.objects.filter(organizer=request.user)
        if not events:
            return Response({
                "response": 1,
                "message": "You have not created any events.",
                "events": []
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(events, many=True)
        return Response({
            "response": 0,
            "message": "Your events retrieved successfully.",
            "events": serializer.data
        }, status=status.HTTP_200_OK)
        
class AttendanceViewSet(ModelViewSet):
    """
    ViewSet to handle RSVP operations for events.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        attendance = serializer.save()
        return Response({
            "response": 0,
            "message": "RSVP created successfully.",
            "attendance": AttendanceSerializer(attendance).data
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        """
        List all RSVPs for the authenticated user.
        """
        if request.user.user_type == "organizer":
            attendances = Attendance.objects.filter(event__organizer=request.user)
        else:
            attendances = Attendance.objects.filter(user=request.user)
        serializer = self.get_serializer(attendances, many=True)
        return Response({
            "response": 0,
            "message": "Your RSVPs retrieved successfully.",
            "attendances": serializer.data
        }, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def approve_rsvp(self, request, pk=None):
        """
        Approve an RSVP for an event.
        """
        attendance = self.get_object()
        if attendance.event.organizer != request.user:
            return Response({
                "response": 1,
                "message": "You do not have permission to approve this RSVP.",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
        
        attendance.approved = True
        attendance.save()
        return Response({
            "response": 0,
            "message": "RSVP approved successfully.",
            "attendance": AttendanceSerializer(attendance).data
        }, status=status.HTTP_200_OK)