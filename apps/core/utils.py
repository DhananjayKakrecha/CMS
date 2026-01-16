from apps.users.models import User

def get_jwt_payload(request):
    """
    Extracts validated JWT payload from request.auth
    """
    token = getattr(request, "auth", None)

    if not token:
        return None

    return token.payload

def get_user_from_jwt(request):
    payload = get_jwt_payload(request)
    if not payload:
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

