from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Announcement, Book, BookComment, Feedback, LibraryGenre, SiteSettings

class SignupForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta: model=User; fields=('username','email','password1','password2')

class BookForm(forms.ModelForm):
    genres=forms.ModelMultipleChoiceField(queryset=LibraryGenre.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Book
        fields=['title','author','description','genres','cover_url','cover_image','backdrop_url','backdrop_image','reading_url','download_url','publisher','publication_year','pages','language','rating','featured','is_published']
        widgets={'description':forms.Textarea(attrs={'rows':7}),'reading_url':forms.URLInput(attrs={'placeholder':'https://... Paste the authorized/public reading link'}),'download_url':forms.URLInput(attrs={'placeholder':'https://... Optional authorized download link'}),'cover_url':forms.URLInput(attrs={'placeholder':'https://... Optional cover image URL'}),'backdrop_url':forms.URLInput(attrs={'placeholder':'https://... Optional backdrop image URL'})}

class LibraryGenreForm(forms.ModelForm):
    class Meta:
        model=LibraryGenre; fields=['name','description','show_on_home','order']
        widgets={'description':forms.Textarea(attrs={'rows':4})}

class BookCommentForm(forms.ModelForm):
    class Meta:
        model=BookComment; fields=['text']; widgets={'text':forms.Textarea(attrs={'rows':4,'maxlength':1000,'placeholder':'Write your comment...'})}

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback; fields=['name','email','phone','category','subject','location','preferred_contact','message']
        widgets={'message':forms.Textarea(attrs={'rows':7})}

class AnnouncementForm(forms.ModelForm):
    class Meta: model=Announcement; fields=['message','is_active']; widgets={'message':forms.Textarea(attrs={'rows':3})}

class SiteSettingsForm(forms.ModelForm):
    class Meta: model=SiteSettings; fields=['site_name','tagline','welcome_title','welcome_text','contact_email','contact_phone']; widgets={'welcome_text':forms.Textarea(attrs={'rows':9})}
