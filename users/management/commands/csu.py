from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создать суперпользователя"

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@example.com").exists():
            user = User.objects.create_user(
                username="admin",
                email="admin@example.com",
                password="12345",
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))

