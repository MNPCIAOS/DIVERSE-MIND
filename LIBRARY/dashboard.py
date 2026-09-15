from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AnnouncementForm, BookForm, FeedbackForm, LibraryGenreForm, SiteSettingsForm
from .models import Announcement, Book, BookComment, Feedback, LibraryGenre, SiteSettings

def is_admin(user): return user.is_authenticated and user.is_staff and user.username == settings.CONTENT_ADMIN_USERNAME
admin_required=user_passes_test(is_admin,login_url='login')

@admin_required
def dashboard(request):
    return render(request,'LIBRARY/dashboard.html',{
        'book_count':Book.objects.count(),'published_count':Book.objects.filter(is_published=True).count(),'draft_count':Book.objects.filter(is_published=False).count(),
        'genre_count':LibraryGenre.objects.count(),'comment_count':BookComment.objects.count(),'feedback_count':Feedback.objects.count(),'views':sum(Book.objects.values_list('view_count',flat=True)),
        'downloads':sum(Book.objects.values_list('download_count',flat=True)),'recent_books':Book.objects.prefetch_related('genres').all()[:10]
    })

@admin_required
def book_list(request): return render(request,'LIBRARY/dashboard_books.html',{'books':Book.objects.prefetch_related('genres').all()})
@admin_required
def book_create(request):
    form=BookForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        b=form.save(); messages.success(request,f'“{b.title}” was published successfully.'); return redirect('dashboard_books')
    return render(request,'LIBRARY/dashboard_book_form.html',{'form':form,'heading':'Publish New Book','submit_text':'Publish Book'})
@admin_required
def book_edit(request,pk):
    b=get_object_or_404(Book,pk=pk); form=BookForm(request.POST or None,request.FILES or None,instance=b)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Book updated successfully.'); return redirect('dashboard_books')
    return render(request,'LIBRARY/dashboard_book_form.html',{'form':form,'heading':f'Edit: {b.title}','submit_text':'Save Changes','book':b})
@admin_required
def book_delete(request,pk):
    b=get_object_or_404(Book,pk=pk)
    if request.method=='POST': b.delete(); messages.success(request,'Book deleted.'); return redirect('dashboard_books')
    return render(request,'LIBRARY/dashboard_confirm.html',{'title':'Delete book','message':f'Delete “{b.title}”?','cancel_url':'dashboard_books','delete_url':'dashboard_library_book_delete','object':b})

@admin_required
def genre_list(request): return render(request,'LIBRARY/dashboard_genres.html',{'genres':LibraryGenre.objects.prefetch_related('books').all()})
@admin_required
def genre_create(request):
    form=LibraryGenreForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Genre created.'); return redirect('dashboard_genres')
    return render(request,'LIBRARY/dashboard_genre_form.html',{'form':form,'heading':'Create Library Genre'})
@admin_required
def genre_edit(request,pk):
    g=get_object_or_404(LibraryGenre,pk=pk); form=LibraryGenreForm(request.POST or None,instance=g)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Genre updated.'); return redirect('dashboard_genres')
    return render(request,'LIBRARY/dashboard_genre_form.html',{'form':form,'heading':f'Edit: {g.name}'})
@admin_required
def genre_delete(request,pk):
    g=get_object_or_404(LibraryGenre,pk=pk)
    if request.method=='POST': g.delete(); messages.success(request,'Genre deleted.'); return redirect('dashboard_genres')
    return render(request,'LIBRARY/dashboard_confirm.html',{'title':'Delete genre','message':f'Delete “{g.name}”? Books will remain but lose this genre.','cancel_url':'dashboard_genres','delete_url':'dashboard_library_genre_delete','object':g})

@admin_required
def comments(request): return render(request,'LIBRARY/dashboard_comments.html',{'comments':BookComment.objects.select_related('book','user').all()})
@admin_required
def comment_delete(request,pk):
    c=get_object_or_404(BookComment,pk=pk)
    if request.method=='POST': c.delete(); messages.success(request,'Comment deleted.'); return redirect('dashboard_comments')
    return render(request,'LIBRARY/dashboard_confirm.html',{'title':'Delete comment','message':'Delete this reader comment?','cancel_url':'dashboard_comments','delete_url':'dashboard_library_comment_delete','object':c})

@admin_required
def feedback(request): return render(request,'LIBRARY/dashboard_feedback.html',{'feedback':Feedback.objects.all()})
@admin_required
def feedback_delete(request,pk):
    f=get_object_or_404(Feedback,pk=pk)
    if request.method=='POST': f.delete(); return redirect('dashboard_feedback')
    return render(request,'LIBRARY/dashboard_confirm.html',{'title':'Delete feedback','message':'Delete this feedback?','cancel_url':'dashboard_feedback','delete_url':'dashboard_library_feedback_delete','object':f})

@admin_required
def announcements(request): return render(request,'LIBRARY/dashboard_announcements.html',{'announcements':Announcement.objects.all()})
@admin_required
def announcement_create(request):
    form=AnnouncementForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Announcement saved.'); return redirect('dashboard_announcements')
    return render(request,'LIBRARY/dashboard_announcement_form.html',{'form':form,'heading':'New Announcement'})
@admin_required
def announcement_edit(request,pk):
    a=get_object_or_404(Announcement,pk=pk); form=AnnouncementForm(request.POST or None,instance=a)
    if request.method=='POST' and form.is_valid(): form.save(); return redirect('dashboard_announcements')
    return render(request,'LIBRARY/dashboard_announcement_form.html',{'form':form,'heading':'Edit Announcement'})
@admin_required
def announcement_delete(request,pk):
    a=get_object_or_404(Announcement,pk=pk)
    if request.method=='POST': a.delete(); return redirect('dashboard_announcements')
    return render(request,'LIBRARY/dashboard_confirm.html',{'title':'Delete announcement','message':'Delete this announcement?','cancel_url':'dashboard_announcements','delete_url':'dashboard_library_announcement_delete','object':a})

@admin_required
def site_settings(request):
    obj=SiteSettings.objects.first() or SiteSettings.objects.create()
    form=SiteSettingsForm(request.POST or None,instance=obj)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Library settings updated.'); return redirect('dashboard_settings')
    return render(request,'LIBRARY/dashboard_site_settings.html',{'form':form})
