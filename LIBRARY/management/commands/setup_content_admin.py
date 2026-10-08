import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Create the initial Diverse Mind Library administrator account if one does not already exist.'

    def add_arguments(self, parser):
        parser.add_argument('--username', default=settings.CONTENT_ADMIN_USERNAME)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username'].strip()
        if not username:
            raise CommandError('CONTENT_ADMIN_USERNAME cannot be empty.')
        password = os.environ.get('CONTENT_ADMIN_PASSWORD', '').strip()

        # Render runs this command on every deploy. Once an administrator exists,
        # never recreate/reset it, so a username/password changed in the dashboard
        # remains changed after redeploys.
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('An administrator already exists; existing administrator credentials were preserved.'))
            return

        if not password:
            raise CommandError('CONTENT_ADMIN_PASSWORD is required when creating the initial administrator.')
        user = User.objects.create(username=username, is_staff=True, is_superuser=True, is_active=True)
        try:
            validate_password(password, user=user)
        except Exception as exc:
            user.delete()
            for error in exc.error_list:
                raise CommandError(f'Password error: {error.message}')
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Initial content administrator '{username}' created successfully."))
