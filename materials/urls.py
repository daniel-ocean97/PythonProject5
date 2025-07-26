from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView, CourseViewSet  # Исправлен импорт

app_name = 'materials'  # Просто строковое значение

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
]