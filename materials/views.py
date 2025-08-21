import stripe
from rest_framework import generics, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import FRONTEND_CANCEL_URL, FRONTEND_SUCCESS_URL
from users.tasks import send_course_update_notifications  # Импорт из другого приложения

from .models import Course, Lesson, Payment
from .paginators import MyPagination
from .permissions import IsOwnerOrManagerForEdit
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsOwnerOrManagerForEdit]
    pagination_class = MyPagination

    def get_queryset(self):
        """Фильтруем курсы: менеджеры видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name="Managers").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании"""
        serializer.save(owner=self.request.user)

        def perform_update(self, serializer):
            # Сохраняем курс
            instance = serializer.save()

            # Запускаем асинхронную задачу для отправки уведомлений
            send_course_update_notifications.delay(instance.id)

            return instance

    def create(self, request, *args, **kwargs):
        """Запрещаем создание менеджерам"""
        if request.user.groups.filter(name="Managers").exists():
            return Response(
                {"detail": "Managers cannot create courses"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Запрещаем удаление менеджерам"""
        if request.user.groups.filter(name="Managers").exists():
            return Response(
                {"detail": "Managers cannot delete courses"},
                status=status.HTTP_403_FORBIDDEN,
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
        if user.groups.filter(name="Managers").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Автоматически назначаем владельца при создании"""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Запрещаем создание менеджерам"""
        if request.user.groups.filter(name="Managers").exists():
            return Response(
                {"detail": "Managers cannot create lessons"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrManagerForEdit]

    def destroy(self, request, *args, **kwargs):
        """Запрещаем удаление менеджерам"""
        if request.user.groups.filter(name="Managers").exists():
            return Response(
                {"detail": "Managers cannot delete lessons"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    # Поля для фильтрации
    search_fields = [
        "course",
        "lesson",
        "payment_method",
    ]

    # Поля для сортировки
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # Сортировка по умолчанию


class CreatePaymentView(APIView):
    """Создание платежной сессии и немедленная проверка статуса"""

    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        user = request.user

        # Создаем сессию оплаты
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": course.stripe_price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{FRONTEND_SUCCESS_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_CANCEL_URL}/cancel",
        )

        # Сохраняем платеж в БД
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            stripe_session_id=session.id,
            status="pending",
        )

        return Response({"session_url": session.url})


class PaymentSuccessView(APIView):
    """Проверка статуса платежа после возврата пользователя"""

    def get(self, request):
        session_id = request.query_params.get("session_id")

        try:
            # Проверяем статус платежа
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                payment = Payment.objects.get(stripe_session_id=session_id)
                payment.status = "paid"
                payment.save()

                return Response({"status": "success", "message": "Оплата подтверждена"})

            return Response({"status": "failed", "message": "Оплата не прошла"})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
