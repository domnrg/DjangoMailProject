from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from mailings.models import Mailing, Message, Client

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт группу 'Managers' (Менеджеры) и назначает ей необходимые права"

    def add_arguments(self, parser):
        parser.add_argument(
            "--name", default="Managers", help="Имя группы (по умолчанию 'Managers')"
        )
        parser.add_argument(
            "--assign",
            nargs="*",
            help="Список email пользователей, которых нужно добавить в группу",
        )

    def handle(self, *args, **options):
        group_name = options["name"]
        assign_emails = options.get("assign") or []

        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' создана"))
        else:
            self.stdout.write(
                self.style.WARNING(f"Группа '{group_name}' уже существует")
            )

        perms_to_add = []

        # view/change perms для моделей mailings
        for model, add_view, add_change, add_delete in (
            (Mailing, True, True, False),  # view + change (для отключения)
            (Message, True, False, False),  # только view
            (Client, True, False, False),  # только view
        ):
            ct = ContentType.objects.get_for_model(model)
            if add_view:
                try:
                    perms_to_add.append(
                        Permission.objects.get(
                            content_type=ct, codename=f"view_{model._meta.model_name}"
                        )
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Permission view_{model._meta.model_name} не найден для {model}"
                        )
                    )
            if add_change:
                try:
                    perms_to_add.append(
                        Permission.objects.get(
                            content_type=ct, codename=f"change_{model._meta.model_name}"
                        )
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Permission change_{model._meta.model_name} не найден для {model}"
                        )
                    )
            if add_delete:
                try:
                    perms_to_add.append(
                        Permission.objects.get(
                            content_type=ct, codename=f"delete_{model._meta.model_name}"
                        )
                    )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Permission delete_{model._meta.model_name} не найден для {model}"
                        )
                    )

        # права на работу с пользователями (view + change для блокировки)
        try:
            ct_user = ContentType.objects.get_for_model(User)
            perms_to_add.append(
                Permission.objects.get(content_type=ct_user, codename="view_user")
            )
            perms_to_add.append(
                Permission.objects.get(content_type=ct_user, codename="change_user")
            )
        except Permission.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"Permission for User not found: {e}"))

        # добавляем все найденные права в группу
        for perm in perms_to_add:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS(f"Назначены права группе '{group_name}'"))

        # добавляем конкретных пользователей в группу (по email)
        if assign_emails:
            for email in assign_emails:
                try:
                    u = User.objects.get(email=email)
                    u.groups.add(group)
                    u.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Пользователь {email} добавлен в группу '{group_name}'"
                        )
                    )
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"Пользователь с email {email} не найден")
                    )

        self.stdout.write(self.style.SUCCESS("Готово."))
