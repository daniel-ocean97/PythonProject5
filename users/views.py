from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from .models import Payment, User
from .serializers import PaymentSerializer

from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]  # Требуем аутентификацию для всех операций

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        # Разрешаем создание (регистрацию) без аутентификации
        if self.action == 'create':
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
            headers=headers
        )

class PaymentViewSet(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    # Поля для фильтрации
    search_fields = [
        'course',
        'lesson',
        'payment_method',
    ]

    # Поля для сортировки
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # Сортировка по умолчанию
