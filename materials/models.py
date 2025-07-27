from django.db import models
from config.settings import AUTH_USER_MODEL

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
        related_name='lessons',
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