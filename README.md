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
