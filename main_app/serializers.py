from rest_framework import serializers
from .models import Service, Caregiver, Appointment, EHR, EHRNote, Review
from django.contrib.auth.models import User

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class CaregiverSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Caregiver
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    patient_id_input = serializers.CharField(write_only=True, required=False, allow_blank=True)
    name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    age = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=EHR.GENDER_CHOICES, write_only=True, required=False, allow_blank=True)
    location = serializers.CharField(write_only=True, required=False, allow_blank=True)
    image = serializers.CharField(write_only=True, required=False, allow_blank=True)
    patient_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'patient_id', 'patient_id_input', 
                   'name', 'phone', 'age', 'gender', 'location', 'image')

    def get_patient_id(self, obj):
        try:
            return obj.ehr.patient_id
        except:
            return None

    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id_input', None)
        name = validated_data.pop('name', None)
        phone = validated_data.pop('phone', None)
        age = validated_data.pop('age', None)
        gender = validated_data.pop('gender', None)
        location = validated_data.pop('location', None)
        image = validated_data.pop('image', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  
        )
        
        EHR.objects.create(
            user=user,
            patient_id=patient_id,
            name=name or '',
            phone=phone or '',
            age=age,
            gender=gender or '',
            location=location or '',
            image=image or ''
        )
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('patient_id_input', None)
        representation.pop('name', None)
        representation.pop('phone', None)
        representation.pop('age', None)
        representation.pop('gender', None)
        representation.pop('location', None)
        representation.pop('image', None)
        return representation

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    caregiver = CaregiverSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    caregiver_id = serializers.IntegerField(write_only=True, required=False)
    service_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Appointment
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['status'] = 'confirmed'
        return super().create(validated_data)


class EHRNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EHRNote
        fields = '__all__'


class EHRSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    appointments = AppointmentSerializer(many=True, read_only=True)
    notes = EHRNoteSerializer(many=True, read_only=True)
    
    class Meta:
        model = EHR
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    service = ServiceSerializer(read_only=True)
    service_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
    
    def get_user(self, obj):
        user_data = {
            'id': obj.user.id,
            'username': obj.user.username
        }
        try:
            if hasattr(obj.user, 'ehr'):
                user_data['name'] = obj.user.ehr.name or obj.user.username
                user_data['image'] = obj.user.ehr.image or ''
        except:
            pass
        return user_data
    
    def create(self, validated_data):
        validated_data.pop('service_id', None)
        service_id = self.initial_data.get('service_id')
        if service_id:
            from .models import Service
            validated_data['service'] = Service.objects.get(id=service_id)
        return super().create(validated_data)