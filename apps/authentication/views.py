from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import User
from apps.otp.services import create_and_send_otp
from .serializers import LoginSerializer

from apps.otp.services import verify_otp
from .serializers import OTPVerifySerializer
from .jwt import generate_tokens


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        create_and_send_otp(user)

        return Response(
            {
                "message": "OTP sent to registered email",
                "otp_required": True
            },
            status=status.HTTP_200_OK
        )

class OTPVerifyView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not verify_otp(user, otp):
            return Response(
                {"detail": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = generate_tokens(user)

        return Response(
            {
                "message": "Login successful",
                "tokens": tokens,
            },
            status=status.HTTP_200_OK
        )
