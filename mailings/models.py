from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    """Получатель рассылки"""
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    # owner = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name="clients",
    #     verbose_name="Владелец",
    #     null=True,
    #     blank=True
    # )

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    """Сообщение для рассылки"""
    subject = models.CharField(max_length=100, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    # owner = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name="messages",
    #     verbose_name="Владелец",
    #     null=True,
    #     blank=True
    # )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    """Рассылка"""
    start_time = models.DateTimeField(verbose_name="Дата и время начала отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")

    STATUS_CHOICES = [
        ('создана', 'Создана'),
        ('запущена', 'Запущена'),
        ('завершена', 'Завершена'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='создана',
        verbose_name="Статус"
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение"
    )

    clients = models.ManyToManyField(
        Client,
        related_name="mailings",
        verbose_name="Получатели"
    )

    # owner = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name="mailings",
    #     verbose_name="Владелец",
    #     null=True,
    #     blank=True
    # )

    def __str__(self):
        return f"Рассылка №{self.pk} ({self.status})"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
