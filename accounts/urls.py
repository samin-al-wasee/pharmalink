from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import UserAuthDetail, UserCreate

urlpatterns = [
    path("/accounts/", include("rest_framework.urls")),
    path("/accounts/register", UserCreate.as_view(), name="user-create"),
    path(
        "/accounts/token/obtain",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path("/accounts/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("/accounts/me", UserAuthDetail.as_view(), name="user-auth-detail"),
]
