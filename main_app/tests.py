from django.test import TestCase
from django.contrib.auth.models import User
from .models import EHR, EHRNote, Service, Caregiver, Appointment, Review
from datetime import date, time

class ModelsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345', email='test1@example.com')
        self.user2 = User.objects.create_user(username='testuser2', password='12345', email='test2@example.com')
        
        self.service1 = Service.objects.create(
            service_name='Home Care',
            description='Basic home care services',
            price_per_hour=50.00,
            duration_options='1day,1month,3months'
        )
        self.service2 = Service.objects.create(
            service_name='Medical Care',
            description='Professional medical care',
            price_per_hour=75.00,
            duration_options='1day,1month'
        )
        self.service3 = Service.objects.create(
            service_name='Physical Therapy',
            description='Physical therapy sessions',
            price_per_hour=60.00
        )
        
        self.caregiver1 = Caregiver.objects.create(
            name='Sarah Johnson',
            speciality='Home Care Specialist',
            bio='Experienced home care provider'
        )
        self.caregiver2 = Caregiver.objects.create(
            name='Dr. Ahmed Ali',
            speciality='Medical Doctor',
            bio='Certified medical professional'
        )
        
        self.caregiver1.services.set([self.service1, self.service2])
        self.caregiver2.services.set([self.service2, self.service3])
        
        self.ehr1 = EHR.objects.create(
            user=self.user1,
            patient_id='P001',
            name='John Doe',
            phone='0501234567',
            age=75,
            gender='male',
            location='Riyadh, Saudi Arabia'
        )
        self.ehr2 = EHR.objects.create(
            user=self.user2,
            patient_id='P002',
            name='Jane Smith',
            phone='0507654321',
            age=68,
            gender='female',
            location='Jeddah, Saudi Arabia'
        )
        
        self.note1 = EHRNote.objects.create(
            ehr=self.ehr1,
            note_text='Patient showing good progress with medication'
        )
        self.note2 = EHRNote.objects.create(
            ehr=self.ehr1,
            note_text='Follow-up appointment recommended'
        )
        self.note3 = EHRNote.objects.create(
            ehr=self.ehr2,
            note_text='Initial assessment completed'
        )
        
        self.appointment1 = Appointment.objects.create(
            user=self.user1,
            caregiver=self.caregiver1,
            service=self.service1,
            date=date(2025, 2, 15),
            time=time(10, 0),
            duration_type='1day',
            start_date=date(2025, 2, 15),
            status='confirmed',
            notes='Morning visit requested'
        )
        self.appointment2 = Appointment.objects.create(
            user=self.user1,
            caregiver=self.caregiver2,
            service=self.service2,
            date=date(2025, 2, 20),
            time=time(14, 30),
            duration_type='1month',
            start_date=date(2025, 2, 20),
            end_date=date(2025, 3, 20),
            status='pending'
        )
        self.appointment3 = Appointment.objects.create(
            user=self.user2,
            caregiver=self.caregiver1,
            service=self.service1,
            date=date(2025, 2, 18),
            time=time(9, 0),
            duration_type='3months',
            start_date=date(2025, 2, 18),
            end_date=date(2025, 5, 18),
            status='completed'
        )
        
        self.review1 = Review.objects.create(
            user=self.user1,
            service=self.service1,
            rating=5,
            comment='Excellent service, very professional'
        )
        self.review2 = Review.objects.create(
            user=self.user1,
            service=self.service2,
            rating=4,
            comment='Good medical care, highly recommended'
        )
        self.review3 = Review.objects.create(
            user=self.user2,
            service=self.service1,
            rating=5,
            comment='Outstanding care and attention'
        )

    def test_user_create(self):
        self.assertEqual(str(self.user1), 'testuser1')
        self.assertEqual(str(self.user2), 'testuser2')

    def test_service_create(self):
        self.assertEqual(str(self.service1), 'Home Care')
        self.assertEqual(str(self.service2), 'Medical Care')
        self.assertEqual(str(self.service3), 'Physical Therapy')

    def test_caregiver_create(self):
        self.assertEqual(str(self.caregiver1), 'Sarah Johnson - Home Care Specialist')
        self.assertEqual(str(self.caregiver2), 'Dr. Ahmed Ali - Medical Doctor')

    def test_ehr_create(self):
        self.assertEqual(str(self.ehr1), 'P001 - testuser1')
        self.assertEqual(str(self.ehr2), 'P002 - testuser2')

    def test_ehrnote_create(self):
        self.assertIn('P001', str(self.note1))
        self.assertIn('P001', str(self.note2))
        self.assertIn('P002', str(self.note3))

    def test_appointment_create(self):
        self.assertIn('testuser1', str(self.appointment1))
        self.assertIn('Home Care', str(self.appointment1))
        self.assertIn('testuser2', str(self.appointment3))
        self.assertIn('Home Care', str(self.appointment3))

    def test_review_create(self):
        self.assertEqual(str(self.review1), 'Review by testuser1 for Home Care')
        self.assertEqual(str(self.review2), 'Review by testuser1 for Medical Care')
        self.assertEqual(str(self.review3), 'Review by testuser2 for Home Care')

    def test_caregiver_services_relationship(self):
        self.assertEqual(self.caregiver1.services.count(), 2)
        self.assertIn(self.service1, self.caregiver1.services.all())
        self.assertIn(self.service2, self.caregiver1.services.all())
        self.assertEqual(self.caregiver2.services.count(), 2)
        self.assertIn(self.service2, self.caregiver2.services.all())
        self.assertIn(self.service3, self.caregiver2.services.all())

    def test_ehr_user_relationship(self):
        self.assertEqual(self.ehr1.user.username, 'testuser1')
        self.assertEqual(self.ehr2.user.username, 'testuser2')

    def test_ehrnote_ehr_relationship(self):
        self.assertEqual(self.note1.ehr, self.ehr1)
        self.assertEqual(self.note2.ehr, self.ehr1)
        self.assertEqual(self.note3.ehr, self.ehr2)

    def test_appointment_user_relationship(self):
        self.assertEqual(self.appointment1.user, self.user1)
        self.assertEqual(self.appointment2.user, self.user1)
        self.assertEqual(self.appointment3.user, self.user2)

    def test_appointment_caregiver_relationship(self):
        self.assertEqual(self.appointment1.caregiver, self.caregiver1)
        self.assertEqual(self.appointment2.caregiver, self.caregiver2)
        self.assertEqual(self.appointment3.caregiver, self.caregiver1)

    def test_appointment_service_relationship(self):
        self.assertEqual(self.appointment1.service, self.service1)
        self.assertEqual(self.appointment2.service, self.service2)
        self.assertEqual(self.appointment3.service, self.service1)

    def test_review_user_relationship(self):
        self.assertEqual(self.review1.user, self.user1)
        self.assertEqual(self.review2.user, self.user1)
        self.assertEqual(self.review3.user, self.user2)

    def test_review_service_relationship(self):
        self.assertEqual(self.review1.service, self.service1)
        self.assertEqual(self.review2.service, self.service2)
        self.assertEqual(self.review3.service, self.service1)

    def test_ehrnote_ordering(self):
        notes = list(self.ehr1.notes.all())
        self.assertEqual(notes[0], self.note2)
        self.assertEqual(notes[1], self.note1)

    def test_appointment_ordering(self):
        appointments = list(Appointment.objects.filter(user=self.user1))
        self.assertEqual(appointments[0].date, date(2025, 2, 20))
        self.assertEqual(appointments[1].date, date(2025, 2, 15))

    def test_review_ordering(self):
        reviews = list(Review.objects.all())
        self.assertEqual(reviews[0], self.review3)
        self.assertEqual(reviews[1], self.review2)
        self.assertEqual(reviews[2], self.review1)

    def test_deleting_user_cascades_to_ehr(self):
        self.user1.delete()
        self.assertEqual(EHR.objects.count(), 1)

    def test_deleting_user_cascades_to_appointments(self):
        self.user1.delete()
        self.assertEqual(Appointment.objects.count(), 1)

    def test_deleting_user_cascades_to_reviews(self):
        self.user1.delete()
        self.assertEqual(Review.objects.count(), 1)

    def test_deleting_ehr_cascades_to_notes(self):
        self.ehr1.delete()
        self.assertEqual(EHRNote.objects.count(), 1)

    def test_deleting_caregiver_cascades_to_appointments(self):
        self.caregiver1.delete()
        self.assertEqual(Appointment.objects.count(), 1)

    def test_deleting_service_cascades_to_appointments(self):
        self.service1.delete()
        self.assertEqual(Appointment.objects.count(), 2)

    def test_deleting_service_cascades_to_reviews(self):
        self.service1.delete()
        self.assertEqual(Review.objects.count(), 1)
