from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Populate Managers and Regular Users groups with test data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--managers", type=int, default=5, help="Number of manager users to create"
        )
        parser.add_argument(
            "--users", type=int, default=10, help="Number of regular users to create"
        )

    def handle(self, *args, **options):
        # Создаем группы, если их нет
        manager_group, created = Group.objects.get_or_create(name="Managers")
        user_group, created = Group.objects.get_or_create(name="Users")

        # Получаем количество пользователей из аргументов
        num_managers = options["managers"]
        num_users = options["users"]

        # Создаем менеджеров
        self.stdout.write(f"Creating {num_managers} managers...")
        for i in range(num_managers):
            email = f"manager{i + 1}@example.com"
            user, created = User.objects.get_or_create(
                email=email, defaults={"password": "managerpass"}
            )
            if created:
                user.set_password("managerpass")
                user.save()
            manager_group.user_set.add(user)
            self.stdout.write(f"  Created manager: {email}")

        # Создаем обычных пользователей
        self.stdout.write(f"\nCreating {num_users} regular users...")
        for i in range(num_users):
            email = f"user{i + 1}@example.com"
            user, created = User.objects.get_or_create(
                email=email, defaults={"password": "userpass"}
            )
            if created:
                user.set_password("userpass")
                user.save()
            user_group.user_set.add(user)
            self.stdout.write(f"  Created user: {email}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully created {num_managers} managers and {num_users} regular users!"
            )
        )
