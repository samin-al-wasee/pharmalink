from django.http import Http404
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserAccount
from .permissions import IsNotAuthenticated
from .serializers import UserAccountCreateSerializer


# Create your views here.
class UserAccountCreateView(CreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountCreateSerializer
    permission_classes = [IsNotAuthenticated]

    def get_view_name(self):
        return "User Account Create"

    def permission_denied(self, request: Request, message=None, code=None) -> None:
        if request.user.is_staff:
            raise PermissionDenied(
                "Please visit the admin panel to register on behalf of new users."
            )
        if request.user.is_authenticated:
            raise PermissionDenied(
                "You have already signed up and are currently logged in."
            )
        super().permission_denied(request, message, code)
