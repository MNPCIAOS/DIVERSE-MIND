from pathlib import Path
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-local-development-only-change-me')
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,[::1]').split(',') if h.strip()]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
    'django.contrib.messages','django.contrib.staticfiles','LIBRARY',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'DIVERSE_MIND_LIBRARY.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.request','django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages','LIBRARY.context_processors.site_context',
    ]},
}]
WSGI_APPLICATION = 'DIVERSE_MIND_LIBRARY.wsgi.application'
DATABASE_URL = os.environ.get('DATABASE_URL','').strip()
if not DEBUG and not DATABASE_URL:
    raise ImproperlyConfigured('DATABASE_URL is required when DJANGO_DEBUG=0.')
DATABASES = {'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}', conn_max_age=600)}
AUTH_PASSWORD_VALIDATORS = [
 {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
 {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'},
 {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
 {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE='en-us'; TIME_ZONE='Africa/Kigali'; USE_I18N=True; USE_TZ=True
STATIC_URL='/static/'; STATIC_ROOT=BASE_DIR/'staticfiles'; STATICFILES_DIRS=[BASE_DIR/'static']
STATICFILES_STORAGE='whitenoise.storage.CompressedManifestStaticFilesStorage'
MEDIA_URL='/media/'; MEDIA_ROOT=BASE_DIR/'media'
CONTENT_ADMIN_USERNAME=os.environ.get('CONTENT_ADMIN_USERNAME','admin')
LOGIN_URL='/account/login/'; LOGIN_REDIRECT_URL='/'; LOGOUT_REDIRECT_URL='/'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE=None; FILE_UPLOAD_MAX_MEMORY_SIZE=10*1024*1024
if not DEBUG:
    SECURE_SSL_REDIRECT=os.environ.get('SECURE_SSL_REDIRECT','1')=='1'; SESSION_COOKIE_SECURE=True; CSRF_COOKIE_SECURE=True
    SECURE_CONTENT_TYPE_NOSNIFF=True; SECURE_REFERRER_POLICY='same-origin'; SECURE_HSTS_SECONDS=int(os.environ.get('SECURE_HSTS_SECONDS','31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS=True; SECURE_HSTS_PRELOAD=False; X_FRAME_OPTIONS='SAMEORIGIN'
