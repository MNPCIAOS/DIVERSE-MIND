from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LIBRARY', '0003_alter_announcement_options_alter_book_options_and_more'),
    ]
    operations = [
        migrations.CreateModel(
            name='AccountActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('signup','Created account'),('login','Logged in'),('logout','Logged out'),('profile','Updated account'),('read','Opened a book'),('download','Downloaded a book'),('like','Liked a book'),('comment','Posted a comment')], max_length=20)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('path', models.CharField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering':['-created_at']},
        ),
        migrations.AddIndex(model_name='accountactivity', index=models.Index(fields=['user','-created_at'], name='LIBRARY_acc_user_id_0d1a1f_idx')),
        migrations.AddIndex(model_name='accountactivity', index=models.Index(fields=['action','-created_at'], name='LIBRARY_acc_action_2e1a9d_idx')),
    ]
