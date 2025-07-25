from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

class CustomUser(AbstractUser):
    
    user_type_choices = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    )
    
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=user_type_choices, default='attendee')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()