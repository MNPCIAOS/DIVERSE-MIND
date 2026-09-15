from pathlib import Path
import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only-change-me",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"


# ============================================================
# ALLOWED HOSTS
# ============================================================
#
# LOCAL:
#   127.0.0.1
#   localhost
#
# RENDER:
#   your-service.onrender.com
#
# CUSTOM DOMAIN:
#   yourdomain.com
#   www.yourdomain.com
#
# On Render, set DJANGO_ALLOWED_HOSTS in Environment Variables.
# Example:
#
# DJANGO_ALLOWED_HOSTS=
# diverse-mind-library.onrender.com,yourdomain.com,www.yourdomain.com
#
# ============================================================

default_allowed_hosts = [
    "127.0.0.1",
    "localhost",
    "[::1]",
]

render_allowed_hosts = [
    ".onrender.com",
]

environment_allowed_hosts = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "",
).split(",")

ALLOWED_HOSTS = list(
    dict.fromkeys(
        default_allowed_hosts
        + render_allowed_hosts
        + [
            host.strip()
            for host in environment_allowed_hosts
            if host.strip()
        ]
    )
)


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "LIBRARY",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise serves static files directly from Render.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "DIVERSE_MIND_LIBRARY.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "LIBRARY.context_processors.site_context",
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "DIVERSE_MIND_LIBRARY.wsgi.application"


# ============================================================
# DATABASE
# ============================================================
#
# LOCALHOST:
#   If DATABASE_URL is not set, SQLite is used.
#
# RENDER + SUPABASE:
#   Set DATABASE_URL to your Supabase PostgreSQL connection URL.
#
# Example:
#
# DATABASE_URL=postgresql://postgres:password@host:5432/postgres
#
# Render will then automatically use Supabase PostgreSQL.
#
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# LANGUAGE / TIME
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Kigali"

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# Only add the root static directory if it actually exists.
ROOT_STATIC_DIR = BASE_DIR / "static"

if ROOT_STATIC_DIR.exists():
    STATICFILES_DIRS = [
        ROOT_STATIC_DIR,
    ]

# WhiteNoise storage
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# ADMIN
# ============================================================

CONTENT_ADMIN_USERNAME = os.environ.get(
    "CONTENT_ADMIN_USERNAME",
    "admin",
)


# ============================================================
# LOGIN / LOGOUT
# ============================================================

LOGIN_URL = "/account/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# FILE UPLOAD SETTINGS
# ============================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = None

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    # HTTPS
    SECURE_SSL_REDIRECT = (
        os.environ.get(
            "SECURE_SSL_REDIRECT",
            "1",
        )
        == "1"
    )

    # Secure cookies
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_REFERRER_POLICY = "same-origin"

    # HSTS
    SECURE_HSTS_SECONDS = int(
        os.environ.get(
            "SECURE_HSTS_SECONDS",
            "31536000",
        )
    )

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = False

    # Allow same-origin framing if needed by the library.
    X_FRAME_OPTIONS = "SAMEORIGIN"


# ============================================================
# CSRF TRUSTED ORIGINS
# ============================================================
#
# Required by Django when using HTTPS on Render.
#
# Add your Render URL automatically.
#
# You can also add your custom domain through:
#
# CSRF_TRUSTED_ORIGINS=
# https://yourdomain.com,https://www.yourdomain.com
#
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

environment_csrf_origins = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "",
).split(",")

CSRF_TRUSTED_ORIGINS.extend(
    [
        origin.strip()
        for origin in environment_csrf_origins
        if origin.strip()
    ]
)


# ============================================================
# RENDER / PROXY SETTINGS
# ============================================================
#
# Render terminates HTTPS before forwarding requests to Django.
# This tells Django to trust Render's HTTPS forwarding header.
#
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ============================================================
# SESSION SETTINGS
# ============================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False


# ============================================================
# OPTIONAL EMAIL SETTINGS
# ============================================================

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "Diverse Mind Library <noreply@diversemindlibrary.com>",
)