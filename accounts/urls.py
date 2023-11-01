from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import UserAuthDetail, UserCreate

urlpatterns = [
    path("/", include("rest_framework.urls")),
    path("/register", UserCreate.as_view(), name="user-create"),
    path(
        "/token/obtain",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path("/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("/me", UserAuthDetail.as_view(), name="user-auth-detail"),
]
