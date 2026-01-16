from rest_framework.permissions import BasePermission
from .utils import get_jwt_payload

class BaseJWTPermission(BasePermission):
    def has_permission(self, request, view):
        payload = get_jwt_payload(request)
        return payload is not None

class IsSuperAdmin(BaseJWTPermission):
    def has_permission(self, request, view):
        payload = get_jwt_payload(request)
        if not payload:
            return False

        return payload.get("role") == "SUPER_ADMIN"

class IsAdmin(BaseJWTPermission):
    def has_permission(self, request, view):
        payload = get_jwt_payload(request)
        if not payload:
            return False

        return payload.get("role") in ["ADMIN", "SUPER_ADMIN"]

class HasCMSAccess(BaseJWTPermission):
    def has_permission(self, request, view):
        payload = get_jwt_payload(request)
        if not payload:
            return False

        if payload.get("role") == "SUPER_ADMIN":
            return True

        return payload.get("can_access") is True

class IsOTPVerified(BaseJWTPermission):
    def has_permission(self, request, view):
        payload = get_jwt_payload(request)
        return payload is not None
