from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Subscription, User
from .serializers import (SubscriptionCreateSerializer, SubscriptionSerializer,
                          UserCreateSerializer, UserSerializer,
                          UserUpdateSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Требуем аутентификацию для всех операций

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        # Разрешаем создание (регистрацию) без аутентификации
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        # Пользователь может работать только со своим профилем
        obj = super().get_object()
        if obj != self.request.user:
            self.permission_denied(self.request)
        return obj


class UserLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]  # Доступно анонимам

    def post(self, request):
        pass


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]  # Доступно анонимам

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Пользователь успешно зарегистрирован"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class SubscriptionCreateView(generics.CreateAPIView):
    """Создание новой подписки"""

    serializer_class = SubscriptionCreateSerializer

    def create(self, request, *args, **kwargs):
        # Проверяем существование подписки
        course_id = request.data.get("course")
        if Subscription.objects.filter(user=request.user, course_id=course_id).exists():
            return Response(
                {"detail": "Подписка на этот курс уже существует"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создаем подписку
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save(user=request.user, is_active=True)

        # Возвращаем полные данные подписки
        full_serializer = SubscriptionSerializer(subscription)
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)


class SubscriptionDeleteView(generics.DestroyAPIView):
    """Удаление подписки"""

    lookup_field = "course_id"

    def get_object(self):
        # Ищем подписку по пользователю и курсу
        course_id = self.kwargs["course_id"]
        try:
            return Subscription.objects.get(user=self.request.user, course_id=course_id)
        except Subscription.DoesNotExist:
            raise NotFound("Подписка на этот курс не найдена")

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
