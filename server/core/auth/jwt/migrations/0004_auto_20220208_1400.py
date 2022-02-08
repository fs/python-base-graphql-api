# Generated by Django 3.2.6 on 2022-02-08 11:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jwt', '0003_delete_resettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='refreshtoken',
            name='expires_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='refreshtoken',
            name='parent_token',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT,
                                       related_name='substitution_token', to='jwt.refreshtoken'),
        ),
    ]
