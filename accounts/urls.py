from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserAccountAuthDetailView, UserAccountCreateView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("register", UserAccountCreateView.as_view(), name="user_account_create"),
    path("token/obtain", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", UserAccountAuthDetailView.as_view(), name="user_account_auth_detail"),
]
