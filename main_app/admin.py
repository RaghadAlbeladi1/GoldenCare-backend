# main_app/admin.py
from django.contrib import admin
from .models import Service, Caregiver

admin.site.register(Service)
admin.site.register(Caregiver)