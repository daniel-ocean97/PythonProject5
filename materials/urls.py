from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from apps import MaterialsConfig

app_name = MaterialsConfig.name

# Для Course (Viewset)
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    # Course endpoints
    path('', include(router.urls)),

    # Lesson endpoints
    path('lessons/', views.LessonListCreateAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
]