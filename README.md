# Diverse Mind Library

A Django-powered digital library based on the architecture and useful interaction patterns of the original project, transformed into a library-only application.

## Features
- Search books by title, author, topic, publisher and language.
- Publish books from the custom administrator dashboard using public/authorized reading links.
- Optional cover/backdrop URLs or uploaded images.
- Optional download links.
- Book views, downloads, likes and reader comments.
- Featured and published/draft controls.
- Eight core homepage genres plus additional genres available through **View More**.
- Genre pages show books belonging to that genre.
- Login, account creation and profile pages.
- Feedback and announcements management.
- Editable welcome copy from Site Settings.
- Day/Night mode and 50 library/nature-inspired themes stored in the browser.
- Render-ready configuration with SQLite locally and PostgreSQL via `DATABASE_URL` in production.

## Local setup
No virtual environment is required by this project.

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py setup_content_admin
python manage.py runserver
```

Open `/` for the library and `/dashboard/` for the content administrator dashboard.

## Render deployment

The Render configuration is designed so no paid Render Shell is required for normal database initialization. `build.sh` installs dependencies and collects static files. Each time the Render web service starts after a deployment, `deploy.sh` runs Django migrations, creates/repairs the single configured content administrator from `CONTENT_ADMIN_USERNAME` and `CONTENT_ADMIN_PASSWORD`, collects static files, and then starts Gunicorn.

Set these Render environment variables:

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` (Render can generate this)
- `DJANGO_ALLOWED_HOSTS` (for example `diverse-mind.onrender.com`)
- `CONTENT_ADMIN_USERNAME=admin`
- `CONTENT_ADMIN_PASSWORD=<your strong password>`
- `DATABASE_URL=<your Supabase PostgreSQL connection string>`

Do not put the real password or database URL into GitHub. Keep them in Render Environment Variables.
