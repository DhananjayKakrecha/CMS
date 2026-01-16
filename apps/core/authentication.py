from rest_framework_simplejwt.authentication import JWTAuthentication

class StatelessJWTAuthentication(JWTAuthentication):
    """
    JWT auth that DOES NOT resolve Django user.
    Returns (None, validated_token).
    """

    def get_user(self, validated_token):
        # ❌ Do NOT touch database
        return None
