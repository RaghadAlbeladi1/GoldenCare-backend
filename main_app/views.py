from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Service, Caregiver, Appointment, EHR, EHRNote, Review
from .serializers import ServiceSerializer, CaregiverSerializer, UserSerializer, AppointmentSerializer, EHRSerializer, EHRNoteSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

class Home(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to GoldenCare API'}, status=status.HTTP_200_OK)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            
            if email and password:
                try:
                    user = User.objects.get(email=email)
                    
                    if user.check_password(password):
                        authenticated_user = authenticate(username=user.username, password=password)
                        
                        if authenticated_user:
                            tokens = RefreshToken.for_user(authenticated_user)
                            content = { 
                                "refresh": str(tokens),  
                                "access": str(tokens.access_token),
                                "user": UserSerializer(authenticated_user).data
                            }
                            return Response(content, status=status.HTTP_200_OK)
                        else:
                            tokens = RefreshToken.for_user(user)
                            content = { 
                                "refresh": str(tokens),  
                                "access": str(tokens.access_token),
                                "user": UserSerializer(user).data
                            }
                            return Response(content, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    pass
                except Exception as error:
                    pass
            
            return Response({"error": "Invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyUserView(APIView):
    permission_classes = []
    
    def get(self, request):
        try:
            if request.user.is_authenticated:
                user = User.objects.get(username=request.user.username)
                try:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': UserSerializer(user).data
                    }, status=status.HTTP_200_OK)
                except Exception as tokenError:
                    return Response({
                        "detail": "Failed to generate token.", 
                        "error": str(tokenError)
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            return Response({
                "detail": "Unexpected error occurred.", 
                "error": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                refresh = RefreshToken(refresh_token)
                user = User.objects.get(id=refresh['user_id'])
                new_refresh = RefreshToken.for_user(user)
                
                return Response({
                    'refresh': str(new_refresh),
                    'access': str(new_refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            except Exception as tokenError:
                return Response({
                    "error": "Invalid refresh token", 
                    "detail": str(tokenError)
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            return Response({
                "error": "Unexpected error occurred.", 
                "detail": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServicesIndex(APIView):
    serializer_class = ServiceSerializer

    def get(self, request):
        try:
            queryset = Service.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CaregiversIndex(APIView):
    serializer_class = CaregiverSerializer

    def get(self, request):
        try:
            queryset = Caregiver.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentsIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get(self, request):
        try:
            queryset = Appointment.objects.filter(user=request.user)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                start_date = serializer.validated_data.get('start_date') or serializer.validated_data.get('date')
                duration_type = serializer.validated_data.get('duration_type', '1day')
                
                if duration_type == '1day':
                    end_date = start_date + timedelta(days=1)
                elif duration_type == '1month':
                    end_date = start_date + relativedelta(months=1)
                elif duration_type == '3months':
                    end_date = start_date + relativedelta(months=3)
                else:
                    end_date = start_date
                
                appointment = serializer.save(
                    user_id=request.user.id,
                    caregiver_id=request.data.get('caregiver'),
                    service_id=request.data.get('service'),
                    start_date=start_date,
                    end_date=end_date
                )
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get(self, request, appointment_id):
        try:
            appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
            serializer = self.serializer_class(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, appointment_id):
        try:
            appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
            serializer = self.serializer_class(appointment, data=request.data, partial=True)
            if serializer.is_valid():
                save_kwargs = {}
                if 'caregiver' in request.data:
                    save_kwargs['caregiver_id'] = request.data.get('caregiver')
                if 'service' in request.data:
                    save_kwargs['service_id'] = request.data.get('service')
                
                start_date_str = request.data.get('start_date') or request.data.get('date')
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                else:
                    start_date = appointment.start_date
                
                duration_type = request.data.get('duration_type') or appointment.duration_type
                
                if duration_type == '1day':
                    end_date = start_date + timedelta(days=1)
                elif duration_type == '1month':
                    end_date = start_date + relativedelta(months=1)
                elif duration_type == '3months':
                    end_date = start_date + relativedelta(months=3)
                else:
                    end_date = start_date
                
                save_kwargs['start_date'] = start_date
                save_kwargs['end_date'] = end_date
                save_kwargs['date'] = start_date
                
                serializer.save(**save_kwargs)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, appointment_id):
        try:
            appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
            appointment.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EHRView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EHRSerializer

    def get(self, request):
        try:
            try:
                ehr = EHR.objects.get(user=request.user)
            except EHR.DoesNotExist:
                patient_id = f"PAT{request.user.id:06d}"
                ehr = EHR.objects.create(
                    user=request.user,
                    patient_id=patient_id,
                    name='',
                    phone='',
                    age=None,
                    gender='',
                    location='',
                    image=''
                )
            serializer = self.serializer_class(ehr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            ehr = EHR.objects.get(user=request.user)
            serializer = self.serializer_class(ehr, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EHR.DoesNotExist:
            return Response({'error': 'EHR not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        return self.put(request)


class EHRNotesIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EHRNoteSerializer

    def get(self, request):
        try:
            ehr = EHR.objects.get(user=request.user)
            notes = EHRNote.objects.filter(ehr=ehr)
            serializer = self.serializer_class(notes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EHR.DoesNotExist:
            return Response({'error': 'EHR not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            ehr = EHR.objects.get(user=request.user)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(ehr=ehr)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EHR.DoesNotExist:
            return Response({'error': 'EHR not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EHRNoteDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EHRNoteSerializer

    def put(self, request, note_id):
        try:
            ehr = EHR.objects.get(user=request.user)
            note = get_object_or_404(EHRNote, id=note_id, ehr=ehr)
            serializer = self.serializer_class(note, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, note_id):
        try:
            ehr = EHR.objects.get(user=request.user)
            note = get_object_or_404(EHRNote, id=note_id, ehr=ehr)
            note.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewsIndex(APIView):
    serializer_class = ReviewSerializer

    def get(self, request):
        try:
            reviews = Review.objects.all().order_by('-created_at')
            serializer = self.serializer_class(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def get(self, request, review_id):
        try:
            review = get_object_or_404(Review, id=review_id)
            serializer = self.serializer_class(review)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, review_id):
        try:
            review = get_object_or_404(Review, id=review_id, user=request.user)
            serializer = self.serializer_class(review, data=request.data, partial=True)
            if serializer.is_valid():
                service_id = request.data.get('service_id')
                if service_id:
                    from .models import Service
                    serializer.save(service=Service.objects.get(id=service_id))
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, review_id):
        try:
            review = get_object_or_404(Review, id=review_id, user=request.user)
            review.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)