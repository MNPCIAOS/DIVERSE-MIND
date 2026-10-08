from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import AccountActivity

@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    AccountActivity.objects.create(user=user, action='login', description='Logged in', path=request.path if request else '')

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user and getattr(user, 'is_authenticated', False):
        AccountActivity.objects.create(user=user, action='logout', description='Logged out', path=request.path if request else '')
