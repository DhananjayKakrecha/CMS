from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Career
from .serializers import CareerSerializer, CareerListSerializer, CareerPublicSerializer

from apps.core.permissions import IsAdmin, HasCMSAccess
from apps.core.utils import get_user_from_jwt

class CareerCMSListView(APIView):
    permission_classes = [IsAdmin, HasCMSAccess]

    def get(self, request):
        careers = Career.objects.all()
        serializer = CareerListSerializer(careers, many=True)
        return Response(serializer.data)

class CareerCreateView(APIView):
    permission_classes = [IsAdmin, HasCMSAccess]

    def post(self, request):
        serializer = CareerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_from_jwt(request)

        career = serializer.save(last_updated_by=user)

        return Response(
            {
                "message": "Career created successfully",
                "id": career.id
            },
            status=status.HTTP_201_CREATED
        )

class CareerUpdateView(APIView):
    permission_classes = [IsAdmin, HasCMSAccess]

    def put(self, request, career_id):
        try:
            career = Career.objects.get(id=career_id)
        except Career.DoesNotExist:
            return Response(
                {"detail": "Career not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CareerSerializer(career, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = get_user_from_jwt(request)

        serializer.save(last_updated_by=user)

        return Response({"message": "Career updated successfully"})

class CareerDeleteView(APIView):
    permission_classes = [IsAdmin, HasCMSAccess]

    def delete(self, request, career_id):
        try:
            career = Career.objects.get(id=career_id)
        except Career.DoesNotExist:
            return Response(
                {"detail": "Career not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        career.delete()
        return Response({"message": "Career deleted successfully"})

class CareerPublicListView(APIView):
    permission_classes = []

    def get(self, request):
        careers = Career.objects.all()
        serializer = CareerPublicSerializer(careers, many=True)
        return Response(serializer.data)
