from django.urls import path
from . import views
urlpatterns=[
 path('',views.home,name='home'),path('search/',views.search,name='search'),path('genres/',views.genres,name='genres'),path('genre/<slug:slug>/',views.genre_detail,name='genre_detail'),
 path('book/<slug:slug>/',views.book_detail,name='book_detail'),path('book/<slug:slug>/read/',views.open_book,name='open_book'),path('book/<slug:slug>/download/',views.download_book,name='download_book'),
 path('book/<slug:slug>/like/',views.toggle_like,name='toggle_like'),path('book/<slug:slug>/comment/',views.add_comment,name='add_comment'),path('comment/<int:comment_id>/delete/',views.delete_comment,name='delete_comment'),
]
