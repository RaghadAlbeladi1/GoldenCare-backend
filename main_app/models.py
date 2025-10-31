from django.db import models
from django.contrib.auth.models import User
img_placeholder="https://img.freepik.com/premium-vector/default-avatar-profile-icon-social-media-user-image-gray-avatar-icon-blank-profile-silhouette-vector-illustration_561158-3407.jpg"


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    duration_options = models.CharField(max_length=100, default="1day,1month,3months")
    imageURL = models.TextField(max_length=100, default=img_placeholder)
    
    def __str__(self):
        return self.service_name



class Caregiver(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    bio = models.TextField(max_length=500)
    imageURL = models.TextField(max_length=100, default=img_placeholder)
    services = models.ManyToManyField(Service, related_name='caregivers')
    
    def __str__(self):
        return f"{self.name} - {self.speciality}"