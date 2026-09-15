#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# Render provides DATABASE_URL at runtime. Run schema setup before starting Django.
python manage.py migrate --noinput
python manage.py setup_content_admin
python manage.py collectstatic --noinput

exec gunicorn DIVERSE_MIND_LIBRARY.wsgi:application --bind 0.0.0.0:${PORT}
