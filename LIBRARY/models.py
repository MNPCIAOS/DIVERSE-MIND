from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def make_slug(value, queryset, instance=None, fallback='item'):
    base = slugify(value) or fallback
    slug = base; n = 2
    qs = queryset.all()
    if instance and instance.pk: qs = qs.exclude(pk=instance.pk)
    while qs.filter(slug=slug).exists():
        slug = f'{base}-{n}'; n += 1
    return slug


class LibraryGenre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    show_on_home = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order','name']; verbose_name='Library genre'; verbose_name_plural='Library genres'
    def save(self,*args,**kwargs):
        self.slug = make_slug(self.name, LibraryGenre.objects, self, 'genre'); super().save(*args,**kwargs)
    def __str__(self): return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    author = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    cover_url = models.URLField(blank=True, help_text='Public cover image URL (optional).')
    cover_image = models.ImageField(upload_to='library/covers/', blank=True)
    backdrop_url = models.URLField(blank=True)
    backdrop_image = models.ImageField(upload_to='library/backdrops/', blank=True)
    reading_url = models.URLField(help_text='Public/authorized link where visitors can read the book.')
    download_url = models.URLField(blank=True, help_text='Optional public/authorized download link.')
    publisher = models.CharField(max_length=180, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1),MaxValueValidator(2100)])
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=80, default='English')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(0),MaxValueValidator(10)])
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveBigIntegerField(default=0)
    download_count = models.PositiveBigIntegerField(default=0)
    genres = models.ManyToManyField(LibraryGenre, related_name='books', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_at']; indexes=[models.Index(fields=['is_published','featured']),models.Index(fields=['publication_year'])]
    def save(self,*args,**kwargs):
        self.slug=make_slug(self.title,Book.objects,self,'book'); super().save(*args,**kwargs)
    @property
    def cover_src(self): return self.cover_image.url if self.cover_image else self.cover_url
    @property
    def backdrop_src(self): return self.backdrop_image.url if self.backdrop_image else self.backdrop_url
    def get_absolute_url(self): return reverse('book_detail',kwargs={'slug':self.slug})
    def __str__(self): return self.title


class BookLike(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='likes')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='book_likes')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['book','user'],name='unique_book_like')]
        indexes=[models.Index(fields=['book','created_at'])]


class BookComment(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='book_comments')
    text=models.TextField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_at']; indexes=[models.Index(fields=['book','-created_at'])]


class Feedback(models.Model):
    CATEGORY_CHOICES=[('feedback','General feedback'),('request','Book request'),('recommendation','Book recommendation'),('problem','Report a problem'),('correction','Content correction'),('partnership','Partnership / business'),('other','Other')]
    CONTACT_CHOICES=[('email','Email'),('phone','Phone call'),('whatsapp','WhatsApp'),('none','No reply needed')]
    name=models.CharField(max_length=120,blank=True); email=models.EmailField(blank=True); phone=models.CharField(max_length=40,blank=True)
    category=models.CharField(max_length=30,choices=CATEGORY_CHOICES,default='feedback'); subject=models.CharField(max_length=200,blank=True)
    location=models.CharField(max_length=160,blank=True); preferred_contact=models.CharField(max_length=20,choices=CONTACT_CHOICES,default='email')
    message=models.TextField(max_length=3000); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return self.subject or f'Feedback from {self.name or "Anonymous"}'


class Announcement(models.Model):
    message=models.CharField(max_length=500); is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return self.message[:80]


class SiteSettings(models.Model):
    site_name=models.CharField(max_length=120,default='Diverse Mind Library')
    tagline=models.CharField(max_length=250,default='Inspiration • Motivation • Opportunities')
    welcome_title=models.CharField(max_length=250,default='What if the knowledge you need is just one click away?')
    welcome_text=models.TextField(default='We’re excited to introduce the “Diverse Mind Library” — a growing space for books, learning, and personal growth.\n\nOne link. Valuable resources. Endless opportunities to learn.\n\nRead. Learn. Grow.\n\n🔔 Coming soon. Stay connected.')
    contact_email=models.EmailField(blank=True); contact_phone=models.CharField(max_length=60,blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.site_name
