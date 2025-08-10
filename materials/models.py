from django.db import models

from config.settings import AUTH_USER_MODEL, STRIPE_SECRET_KEY


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        verbose_name="Превью", null=True, blank=True, upload_to="course_preview/"
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,  # При удалении пользователя курс остаётся
        blank=True,
        null=True,
        verbose_name="Создатель",
    )
    stripe_price_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="ID цены в Stripe"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Цена"
    )

    def save(self, *args, **kwargs):
        """Автоматически создаем продукт в Stripe при сохранении"""
        if not self.stripe_price_id and self.price > 0:
            self.create_stripe_product()
        super().save(*args, **kwargs)

    def create_stripe_product(self):
        import stripe

        stripe.api_key = STRIPE_SECRET_KEY

        product = stripe.Product.create(name=self.name)
        price = stripe.Price.create(
            unit_amount=int(self.price * 100), currency="usd", product=product.id
        )
        self.stripe_price_id = price.id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока")
    preview = models.ImageField(
        verbose_name="Превью", null=True, blank=True, upload_to="lesson_preview/"
    )
    description = models.TextField(verbose_name="Описание")
    video = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,  # Удалять уроки при удалении курса
        related_name="lessons",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,  # При удалении пользователя урок остаётся
        blank=True,
        null=True,
        verbose_name="Создатель",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачено"),
    ]

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
