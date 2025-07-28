from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=35, blank=True, null=True)
    avatar = models.ImageField(
        verbose_name="Аватар", null=True, blank=True, upload_to="users_avatar/"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CASH = 'cash'
    PAYMENT_METHOD_TRANSFER = 'transfer'
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_METHOD_CASH, 'Наличные'),
        (PAYMENT_METHOD_TRANSFER, 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_payments',
        verbose_name="Пользователь"
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты"
    )

    # Ленивые ссылки через строки
    course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_payments',
        verbose_name="Оплаченный курс"
    )

    lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_payments',
        verbose_name="Оплаченный урок"
    )

    amount = models.IntegerField(
        verbose_name="Сумма оплаты"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты"
    )


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    is_active = models.BooleanField(verbose_name="Активность подписки")

    def __str__(self):
        return f"Подписка пользователя {self.user} на курс {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"