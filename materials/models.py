from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        verbose_name="Превью", null=True, blank=True, upload_to="course_preview/"
    )
    description = models.TextField(verbose_name="Описание")

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"