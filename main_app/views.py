from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Service, Caregiver
from .serializers import ServiceSerializer, CaregiverSerializer

class Home(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to GoldenCare API'}, status=status.HTTP_200_OK)

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