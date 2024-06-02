from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token

from bus_routing.serializer import EmailSerializer

class RequestOTPView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = get_random_string(length=6, allowed_chars='0123456789')
            cache.set(email, otp, timeout=300)  # Lưu OTP trong 5 phút
            
            # Gửi OTP qua email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        cached_otp = cache.get(email)
        
        if cached_otp and cached_otp == otp:
            # Xác thực OTP thành công
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            if created:
                user.set_password('default_password')
                user.save()
            
            # Tạo token đăng nhập
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
