from django.contrib import admin
from .models import AccountActivity, Announcement, Book, BookComment, BookLike, Feedback, LibraryGenre, SiteSettings
admin.site.register([Book,LibraryGenre,BookLike,BookComment,Feedback,Announcement,SiteSettings,AccountActivity])
