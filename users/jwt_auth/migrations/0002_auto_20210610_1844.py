# Generated by Django 3.2.4 on 2021-06-10 15:44

from django.utils import timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='refreshtoken',
            name='created_at',
            field=models.DateTimeField(default=timezone.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='refreshtoken',
            name='jti',
            field=models.CharField(default='test', editable=False, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='refreshtoken',
            name='revoked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='refreshtoken',
            unique_together={('token', 'created_at', 'jti')},
        ),
        migrations.RemoveField(
            model_name='refreshtoken',
            name='expires_at',
        ),
    ]
