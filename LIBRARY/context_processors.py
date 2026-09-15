from django.conf import settings
from .models import Announcement, LibraryGenre, SiteSettings

def site_context(request):
    settings_obj = SiteSettings.objects.first()
    return {
        'site_settings': settings_obj,
        'site_announcements': Announcement.objects.filter(is_active=True)[:5],
        'home_genres_nav': LibraryGenre.objects.filter(show_on_home=True)[:8],
        'is_content_admin': request.user.is_authenticated and request.user.is_staff and request.user.username == settings.CONTENT_ADMIN_USERNAME,
    }
