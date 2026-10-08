# Diverse Mind Library

A Django-powered digital library based on the architecture and useful interaction patterns of the original project, transformed into a library-only application.

## Features
- Search books by title, author, topic, publisher and language.
- Publish books from the custom administrator dashboard using public/authorized reading links.
- Optional cover/backdrop URLs or uploaded images. Remote URLs must point directly to an image file/resource; book covers are displayed without forced cropping.
- Optional download links.
- Book views, downloads, likes and reader comments.
- Featured and published/draft controls.
- Eight core homepage genres plus additional genres available through **View More**.
- Genre pages show books belonging to that genre.
- Login, account creation, profile pages, and self-service account username/email/password updates.
- Feedback and announcements management, plus administrator reader-account management and activity history.
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

The Render configuration is designed so no paid Render Shell is required for normal database initialization. `build.sh` installs dependencies and collects static files. Each time the Render web service starts after a deployment, `deploy.sh` runs Django migrations, creates the initial content administrator only if no superuser exists, collects static files, and then starts Gunicorn. This prevents a username or password changed from the dashboard from being overwritten on a later deploy.

Set these Render environment variables:

- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` (Render can generate this)
- `DJANGO_ALLOWED_HOSTS` (for example `diverse-mind.onrender.com`)
- `CONTENT_ADMIN_USERNAME=admin` (used only when the initial administrator is created; later dashboard username changes are preserved)
- `CONTENT_ADMIN_PASSWORD=<your strong password>` (used only for the initial administrator creation; later dashboard password changes are preserved)
- `DATABASE_URL=<your Supabase PostgreSQL connection string>`

Do not put the real password or database URL into GitHub. Keep them in Render Environment Variables.
