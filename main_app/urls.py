from django.urls import path
from .views import (
    Home, 
    ServicesIndex, 
    CaregiversIndex,
    AppointmentsIndex,
    AppointmentDetail,
    EHRView,
    EHRNotesIndex,
    EHRNoteDetail,
    ReviewsIndex,
    ReviewDetail,
    CreateUserView, LoginView, VerifyUserView
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('services/', ServicesIndex.as_view(), name='services-index'),
    path('caregivers/', CaregiversIndex.as_view(), name='caregivers-index'),
    path('appointments/', AppointmentsIndex.as_view(), name='appointments-index'),
    path('appointments/<int:appointment_id>/', AppointmentDetail.as_view(), name='appointment-detail'),
    path('ehr/', EHRView.as_view(), name='ehr'),
    path('ehr/notes/', EHRNotesIndex.as_view(), name='ehr-notes-index'),
    path('ehr/notes/<int:note_id>/', EHRNoteDetail.as_view(), name='ehr-note-detail'),
    path('reviews/', ReviewsIndex.as_view(), name='reviews-index'),
    path('reviews/<int:review_id>/', ReviewDetail.as_view(), name='review-detail'),
]