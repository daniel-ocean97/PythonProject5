from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from materials.models import Course  # Импорт из другого приложения
from users.models import Subscription  # Локальная модель

User = get_user_model()


@shared_task
def send_course_update_notifications(course_id):
    """Отправляет уведомления об обновлении курса"""
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return  # Если курс удален - прекращаем задачу

    subscriptions = Subscription.objects.filter(
        course_id=course_id, is_active=True
    ).select_related("user")

    for subscription in subscriptions:
        user = subscription.user
        subject = f"Обновление курса: {course.title}"
        message = (
            f"Здравствуйте!\n\n"
            f"Курс '{course.name}', на который вы подписаны, был обновлен.\n\n"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    """
    # Рассчитываем дату "месяц назад" с учетом временной зоны
    cutoff_date = timezone.now() - timedelta(days=30)

    # Блокируем пользователей
    result = User.objects.filter(
        last_login__lt=cutoff_date,  # Последний вход раньше cutoff_date
        is_active=True,  # Только активных пользователей
    ).update(is_active=False)

    return f"Заблокировано пользователей: {result}"
