from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserAccountCreateView, UserAccountAuthDetailView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("register", UserAccountCreateView.as_view(), name="user_account_create"),
    path("login/token-obtain", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/token-refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", UserAccountAuthDetailView.as_view(), name="user_account_auth_detail"),
]
