from django.urls import path
from .views import Home, ServicesIndex, CaregiversIndex

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('services/', ServicesIndex.as_view(), name='services-index'),
    path('caregivers/', CaregiversIndex.as_view(), name='caregivers-index'),
]