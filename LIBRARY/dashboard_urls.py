from django.urls import path
from . import dashboard
urlpatterns=[
 path('',dashboard.dashboard,name='dashboard'),path('books/',dashboard.book_list,name='dashboard_books'),path('books/new/',dashboard.book_create,name='dashboard_book_create'),path('books/<int:pk>/edit/',dashboard.book_edit,name='dashboard_book_edit'),path('books/<int:pk>/delete/',dashboard.book_delete,name='dashboard_library_book_delete'),
 path('genres/',dashboard.genre_list,name='dashboard_genres'),path('genres/new/',dashboard.genre_create,name='dashboard_genre_create'),path('genres/<int:pk>/edit/',dashboard.genre_edit,name='dashboard_genre_edit'),path('genres/<int:pk>/delete/',dashboard.genre_delete,name='dashboard_library_genre_delete'),
 path('comments/',dashboard.comments,name='dashboard_comments'),path('comments/<int:pk>/delete/',dashboard.comment_delete,name='dashboard_library_comment_delete'),
 path('feedback/',dashboard.feedback,name='dashboard_feedback'),path('feedback/<int:pk>/delete/',dashboard.feedback_delete,name='dashboard_library_feedback_delete'),
 path('announcements/',dashboard.announcements,name='dashboard_announcements'),path('announcements/new/',dashboard.announcement_create,name='dashboard_announcement_create'),path('announcements/<int:pk>/edit/',dashboard.announcement_edit,name='dashboard_announcement_edit'),path('announcements/<int:pk>/delete/',dashboard.announcement_delete,name='dashboard_library_announcement_delete'),
 path('settings/',dashboard.site_settings,name='dashboard_settings'),
]
