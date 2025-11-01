from django.contrib import admin
from .models import Service, Caregiver, Appointment, EHR, EHRNote

admin.site.site_header = "GoldenCare Administration"
admin.site.site_title = "GoldenCare Admin"
admin.site.index_title = "Welcome to GoldenCare Administration"

admin.site.register(Service)
admin.site.register(Caregiver)
admin.site.register(Appointment)
admin.site.register(EHR)
admin.site.register(EHRNote)