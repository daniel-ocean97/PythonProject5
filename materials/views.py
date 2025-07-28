from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .models import Course, Lesson
from .paginators import MyPagination
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwnerOrManagerForEdit

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrManagerForEdit]
    pagination_class = MyPagination

    def get_queryset(self):
        """Фильтруем курсы: менеджеры видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name='Managers').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании"""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Запрещаем создание менеджерам"""
        if request.user.groups.filter(name='Managers').exists():
            return Response(
                {"detail": "Managers cannot create courses"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Запрещаем удаление менеджерам"""
        if request.user.groups.filter(name='Managers').exists():
            return Response(
                {"detail": "Managers cannot delete courses"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrManagerForEdit]
    pagination_class = MyPagination

    def get_queryset(self):
        """Фильтруем уроки: менеджеры видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name='Managers').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании"""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Запрещаем создание менеджерам"""
        if request.user.groups.filter(name='Managers').exists():
            return Response(
                {"detail": "Managers cannot create lessons"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrManagerForEdit]

    def destroy(self, request, *args, **kwargs):
        """Запрещаем удаление менеджерам"""
        if request.user.groups.filter(name='Managers').exists():
            return Response(
                {"detail": "Managers cannot delete lessons"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)