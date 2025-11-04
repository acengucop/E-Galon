from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import RegisterSerializer, LoginSerializer

def _issue_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "user": {"id": user.id, "username": user.username, "email": user.email or ""},
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    ser = RegisterSerializer(data=request.data)
    if not ser.is_valid():
        return Response({"detail": ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    user = ser.save()
    data = _issue_tokens_for_user(user)  # auto-login setelah register
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    ser = LoginSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    user = authenticate(
        request,
        username=ser.validated_data["username"],
        password=ser.validated_data["password"],
    )
    if not user:
        return Response({"detail": "username/password salah"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(_issue_tokens_for_user(user))

@api_view(["POST"])
def logout(request):
    """
    Logout = blacklist refresh token yang dikirim.
    Body: {"refresh": "<refresh_token>"}
    """
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response({"detail": "refresh token wajib"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # butuh app token_blacklist aktif
    except Exception:
        return Response({"detail": "refresh token invalid"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "logout sukses"})
    
@api_view(["GET"])
def me(request):
    u = request.user
    return Response({"id": u.id, "username": u.username, "email": u.email or ""})
