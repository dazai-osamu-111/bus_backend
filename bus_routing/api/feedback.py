from rest_framework.response import Response
from rest_framework import status

from rest_framework import views

from bus_routing.models import feedback
from bus_routing.serializer import feedbackSerializer

class feedbackView(views.APIView):
    def post(self, request):
        serializer = feedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        feedbacks = feedback.objects.all()
        serializer = feedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)