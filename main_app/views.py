from django.shortcuts import render #besure for this if deleted

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the GoldenCare API home route!'}
    return Response(content)