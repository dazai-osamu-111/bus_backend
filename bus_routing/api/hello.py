from rest_framework.views import APIView
from rest_framework.response import Response


# create apiView to return hello
class BusStationHelloView(APIView):

    def get(self, request):
        return Response(data={'message': 'Hello World!'})