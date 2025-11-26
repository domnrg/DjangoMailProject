from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создать суперпользователя"

    def handle(self, *args, **options):
        email = "admin@example.com"
        password = "12345"

        if not User.objects.filter(email=email).exists():
            user = User(
                email=email,
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
