from django.db import models
from django.contrib.auth.models import User
img_placeholder="https://img.freepik.com/premium-vector/default-avatar-profile-icon-social-media-user-image-gray-avatar-icon-blank-profile-silhouette-vector-illustration_561158-3407.jpg"


class EHR(models.Model):
    """Electronic Health Record - Contains all patient information"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ehr')
    patient_id = models.CharField(max_length=50, unique=True, help_text="Patient Identity ID")
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    image = models.TextField(max_length=500, default=img_placeholder, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient_id} - {self.user.username}"


class EHRNote(models.Model):
    """Notes for EHR - Patient can add multiple notes"""
    ehr = models.ForeignKey(EHR, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.ehr.patient_id} - {self.created_at.strftime('%Y-%m-%d')}"


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


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    DURATION_CHOICES = [
        ('1day', '1 Day'),
        ('1month', '1 Month'),
        ('3months', '3 Months'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    duration_type = models.CharField(max_length=20, choices=DURATION_CHOICES, default='1day')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
    
    def __str__(self):
        return f"{self.user.username} - {self.service.service_name} on {self.date} at {self.time}"