from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user):
    """
    Generates JWT tokens AFTER OTP verification.
    Uses SimpleJWT but embeds ONLY our custom claims.
    """

    # ✅ PASS REAL USER (NOT None)
    refresh = RefreshToken.for_user(user)

    # 🔥 OVERRIDE / ADD custom claims
    refresh["user_id"] = str(user.id)
    refresh["email"] = user.email
    refresh["role"] = user.role
    refresh["can_access"] = True if user.role == "SUPER_ADMIN" else user.can_access

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
