from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('LIBRARY.dashboard_urls')),
    path('account/', include('LIBRARY.account_urls')),
    path('contact/', include('LIBRARY.contact_urls')),
    path('', include('LIBRARY.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
