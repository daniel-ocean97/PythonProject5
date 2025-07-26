from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from .models import Payment
from .serializers import PaymentSerializer


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
