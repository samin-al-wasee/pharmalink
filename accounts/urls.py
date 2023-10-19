from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserAuthDetail, UserCreate

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("register", UserCreate.as_view(), name="user_create"),
    path("token/obtain", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", UserAuthDetail.as_view(), name="user_auth_detail"),
]
