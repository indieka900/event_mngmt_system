from django.db import models
from accounts.models import CustomUser as User
import uuid

class Event(models.Model):
    event_id = models.CharField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    slots_available = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    reg_deadline = models.DateTimeField()
    key_words = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.event_id:
            self.event_id = f"event-{uuid.uuid4()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    rsvp_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"
