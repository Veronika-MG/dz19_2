from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='veronika-mg@mail.ru',
            first_name='Veronika',
            last_name='Melkonyan',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('Veronika262')
        user.save()

