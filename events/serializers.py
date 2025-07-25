from rest_framework import serializers
from events.models import Event, Attendance
from django.contrib.auth import get_user_model
User = get_user_model()

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('event_id', 'created_at', 'organizer')

    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        print(validated_data['organizer'].user_type)
        if validated_data['organizer'].user_type != "organizer":
            raise serializers.ValidationError("You do not have permission to create events.")
        event = Event.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class AttendanceSerializer(serializers.ModelSerializer):
    event_data = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('rsvp_at','user', 'event_data')
        
    def get_event_data(self, obj):
        return EventSerializer(obj.event).data

    def create(self, validated_data):
        user = self.context['request'].user
        # print(type(validated_data['event']))
        event = validated_data['event']
        if Attendance.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("You have already RSVP'd for this event.")
        if event.slots_available <= 0:
            raise serializers.ValidationError("No slots available for this event.")
        attendance = Attendance.objects.create(user=user, **validated_data)
        event.slots_available -= 1
        event.save()
        return attendance