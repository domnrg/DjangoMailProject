from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from mailings.models import Mailing, Attempt


class Command(BaseCommand):
    help = "Отправка всех активных рассылок вручную"

    def handle(self, *args, **options):
        active_mailings = Mailing.objects.filter(status="запущена")

        if not active_mailings.exists():
            self.stdout.write(self.style.WARNING("Нет активных рассылок для отправки."))
            return

        for mailing in active_mailings:
            message = mailing.message

            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    status = "Успешно"
                    server_response = "Письмо отправлено"
                except Exception as e:
                    status = "Не успешно"
                    server_response = str(e)

                # Сохраняем попытку отправки
                Attempt.objects.create(
                    mailing=mailing,
                    attempt_time=timezone.now(),
                    status=status,
                    server_response=server_response,
                )

        self.stdout.write(self.style.SUCCESS("Все активные рассылки обработаны."))
