# Generated by Django 3.2.5 on 2021-07-28 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jwt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resettoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_tokens', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='refreshtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refresh_tokens', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='refreshtoken',
            unique_together={('token', 'created_at', 'jti')},
        ),
    ]
