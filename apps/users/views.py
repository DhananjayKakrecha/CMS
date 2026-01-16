from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import AdminSerializer, AdminListSerializer
from .constants import UserRole
from apps.core.permissions import IsSuperAdmin

class AdminListView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        admins = User.objects.filter(role=UserRole.ADMIN)
        serializer = AdminListSerializer(admins, many=True)
        return Response(serializer.data)

class AdminCreateView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Admin created successfully"},
            status=status.HTTP_201_CREATED
        )

class AdminUpdateView(APIView):
    permission_classes = [IsSuperAdmin]

    def put(self, request, admin_id):
        try:
            admin = User.objects.get(id=admin_id, role=UserRole.ADMIN)
        except User.DoesNotExist:
            return Response(
                {"detail": "Admin not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminSerializer(admin, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Admin updated successfully"})

class AdminDeleteView(APIView):
    permission_classes = [IsSuperAdmin]

    def delete(self, request, admin_id):
        try:
            admin = User.objects.get(id=admin_id, role=UserRole.ADMIN)
        except User.DoesNotExist:
            return Response(
                {"detail": "Admin not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        admin.delete()
        return Response({"message": "Admin deleted successfully"})

class AdminAccessToggleView(APIView):
    permission_classes = [IsSuperAdmin]

    def patch(self, request, admin_id):
        try:
            admin = User.objects.get(id=admin_id, role=UserRole.ADMIN)
        except User.DoesNotExist:
            return Response(
                {"detail": "Admin not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        admin.can_access = not admin.can_access
        admin.save(update_fields=["can_access"])

        return Response({
            "message": "Admin access updated",
            "can_access": admin.can_access
        })
