from django.db import migrations
from django.utils.text import slugify

GENRES=[
 ('Personal Development',True,1),('English Learning',True,2),('General Knowledge',True,3),('Mindset & Motivation',True,4),
 ('Education & Self-Improvement',True,5),('Business & Entrepreneurship',True,6),('Science & Technology',True,7),('Literature & Fiction',True,8),
 ('Health & Wellness',False,20),('History & Culture',False,21),('Finance & Money',False,22),('Leadership',False,23),('Career & Skills',False,24),('Children & Young Readers',False,25),('Religion & Philosophy',False,26),('Arts & Creativity',False,27)
]
def seed(apps,schema_editor):
    Genre=apps.get_model('LIBRARY','LibraryGenre'); Settings=apps.get_model('LIBRARY','SiteSettings')
    for name,home,order in GENRES: Genre.objects.get_or_create(name=name,defaults={'slug':slugify(name),'show_on_home':home,'order':order})
    Settings.objects.get_or_create(id=1)
def unseed(apps,schema_editor): pass
class Migration(migrations.Migration):
    dependencies=[('LIBRARY','0001_initial')]
    operations=[migrations.RunPython(seed,unseed)]
