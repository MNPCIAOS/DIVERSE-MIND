from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Count, F, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BookCommentForm, FeedbackForm, SignupForm
from .models import Book, BookComment, BookLike, Feedback, LibraryGenre

HOME_GENRE_LIMIT=8

def home(request):
    q=request.GET.get('q','').strip()
    books=Book.objects.filter(is_published=True).annotate(like_count=Count('likes',distinct=True)).prefetch_related('genres')
    if q: books=books.filter(Q(title__icontains=q)|Q(author__icontains=q)|Q(description__icontains=q)|Q(publisher__icontains=q)|Q(language__icontains=q)|Q(genres__name__icontains=q)).distinct()
    latest=books.order_by('-created_at')[:12]
    featured=books.filter(featured=True).order_by('-created_at')[:8]
    home_genres=LibraryGenre.objects.filter(show_on_home=True).prefetch_related('books')[:HOME_GENRE_LIMIT]
    genre_sections=[]
    for genre in home_genres:
        row=Book.objects.filter(is_published=True,genres=genre).order_by('-created_at')[:8]
        if row: genre_sections.append({'genre':genre,'books':row})
    return render(request,'LIBRARY/home.html',{'books':books[:24],'latest_books':latest,'featured_books':featured,'home_genres':home_genres,'genre_sections':genre_sections,'query':q})

def search(request):
    q=request.GET.get('q','').strip(); genre=request.GET.get('genre','').strip(); year=request.GET.get('year','').strip(); language=request.GET.get('language','').strip(); rating=request.GET.get('rating','').strip(); sort=request.GET.get('sort','newest').strip()
    books=Book.objects.filter(is_published=True).annotate(like_count=Count('likes',distinct=True)).prefetch_related('genres')
    if q: books=books.filter(Q(title__icontains=q)|Q(author__icontains=q)|Q(description__icontains=q)|Q(publisher__icontains=q)|Q(language__icontains=q)|Q(genres__name__icontains=q))
    if genre: books=books.filter(genres__slug=genre)
    if year.isdigit(): books=books.filter(publication_year=int(year))
    if language: books=books.filter(language__iexact=language)
    try:
        if rating: books=books.filter(rating__gte=float(rating))
    except ValueError: pass
    sort_map={'newest':'-created_at','oldest':'created_at','year_desc':'-publication_year','year_asc':'publication_year','rating':'-rating','title':'title','views':'-view_count','downloads':'-download_count'}
    books=books.order_by(sort_map.get(sort,'-created_at')).distinct()
    page=Paginator(books,24).get_page(request.GET.get('page'))
    years=Book.objects.filter(is_published=True,publication_year__isnull=False).values_list('publication_year',flat=True).distinct().order_by('-publication_year')
    languages=Book.objects.filter(is_published=True).values_list('language',flat=True).distinct().order_by('language')
    return render(request,'LIBRARY/search.html',{'page':page,'genres':LibraryGenre.objects.all(),'years':years,'languages':languages,'query':q,'active_genre':genre,'active_year':year,'active_language':language,'active_rating':rating,'active_sort':sort})

def genres(request):
    all_genres=LibraryGenre.objects.prefetch_related('books').all()
    return render(request,'LIBRARY/genres.html',{'genres':all_genres})

def genre_detail(request,slug):
    genre=get_object_or_404(LibraryGenre,slug=slug)
    books=genre.books.filter(is_published=True).annotate(like_count=Count('likes',distinct=True)).order_by('-created_at')
    return render(request,'LIBRARY/genre_detail.html',{'genre':genre,'books':books})

def book_detail(request,slug):
    book=get_object_or_404(Book.objects.prefetch_related('genres','comments__user'),slug=slug,is_published=True)
    Book.objects.filter(pk=book.pk).update(view_count=F('view_count')+1); book.view_count+=1
    liked=request.user.is_authenticated and BookLike.objects.filter(book=book,user=request.user).exists()
    comments=book.comments.select_related('user').all()[:50]
    return render(request,'LIBRARY/book_detail.html',{'book':book,'liked':liked,'like_count':book.likes.count(),'comments':comments,'form':BookCommentForm()})

@login_required
def toggle_like(request,slug):
    book=get_object_or_404(Book,slug=slug,is_published=True); like,created=BookLike.objects.get_or_create(book=book,user=request.user)
    if not created: like.delete()
    return redirect(book.get_absolute_url())

@login_required
def add_comment(request,slug):
    book=get_object_or_404(Book,slug=slug,is_published=True); form=BookCommentForm(request.POST)
    if request.method=='POST' and form.is_valid():
        c=form.save(commit=False); c.book=book; c.user=request.user; c.save(); messages.success(request,'Your comment was posted.')
    return redirect(book.get_absolute_url())

@login_required
def delete_comment(request,comment_id):
    comment=get_object_or_404(BookComment,pk=comment_id)
    if request.method=='POST' and (comment.user_id==request.user.id or request.user.is_staff): comment.delete()
    return redirect(comment.book.get_absolute_url())

def open_book(request,slug):
    book=get_object_or_404(Book,slug=slug,is_published=True); return redirect(book.reading_url)

def download_book(request,slug):
    book=get_object_or_404(Book,slug=slug,is_published=True)
    if not book.download_url: return redirect(book.get_absolute_url())
    Book.objects.filter(pk=book.pk).update(download_count=F('download_count')+1); return redirect(book.download_url)

def signup(request):
    form=SignupForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); login(request,user); messages.success(request,'Welcome to Diverse Mind Library.'); return redirect('home')
    return render(request,'LIBRARY/signup.html',{'form':form})

class ContentLoginView(LoginView): template_name='LIBRARY/login.html'; redirect_authenticated_user=True

@login_required
def account_profile(request):
    return render(request,'LIBRARY/profile.html',{'books_read':Book.objects.filter(view_count__gt=0).count()})

def contact(request):
    form=FeedbackForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        feedback=form.save(commit=False)
        if request.user.is_authenticated:
            if not feedback.name: feedback.name=request.user.get_full_name() or request.user.username
            if not feedback.email: feedback.email=request.user.email
        feedback.save(); messages.success(request,'Thank you. Your feedback has been received.'); return redirect('contact')
    return render(request,'LIBRARY/contact.html',{'form':form})
