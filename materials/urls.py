from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    CreatePaymentView,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    PaymentSuccessView,
    PaymentViewSet,
)

app_name = "materials"  # Просто строковое значение

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-detail",
    ),
    path("pay/<int:course_id>/", CreatePaymentView.as_view(), name="create-payment"),
    path("payment-success/", PaymentSuccessView.as_view(), name="payment-success"),
]
