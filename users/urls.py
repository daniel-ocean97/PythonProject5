from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.views import (SubscriptionCreateView, SubscriptionDeleteView,
                         UserRegistrationView, UserViewSet)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "subscriptions/", SubscriptionCreateView.as_view(), name="subscription-create"
    ),
    path(
        "subscriptions/<int:course_id>/",
        SubscriptionDeleteView.as_view(),
        name="subscription-delete",
    ),
]

urlpatterns += router.urls
