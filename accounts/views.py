from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsNotAuthenticated
from .serializers import UserAccountSerializer


# Create your views here.
class UserAccountCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserAccountSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsNotAuthenticated]

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


class UserAccountAuthDetailView(RetrieveAPIView):
    serializer_class = UserAccountSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        authenticated_user_account: get_user_model() = request.user
        serializer: UserAccountSerializer = self.get_serializer(
            authenticated_user_account
        )
        return Response(serializer.data)
