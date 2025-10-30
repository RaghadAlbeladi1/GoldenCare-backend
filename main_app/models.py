from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    duration_options = models.CharField(max_length=100, default="1day,1month,3months")
    image = models.URLField(blank=True)
    
    def __str__(self):
        return self.service_name



class Caregiver(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    certifications = models.TextField(max_length=300, blank=True)
    image = models.URLField(blank=True)
    services = models.ManyToManyField(Service, related_name='caregivers')
    
    def __str__(self):
        return f"{self.name} - {self.speciality}"